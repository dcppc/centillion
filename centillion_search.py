import shutil
import html.parser

from gdrive_util import GDrive
from apiclient.http import MediaIoBaseDownload

import mistune
from whoosh.fields import *
import whoosh.index as index
import os, re, io, requests
import tempfile, subprocess
import pypandoc
import os.path
import codecs
from whoosh.qparser import MultifieldParser, QueryParser
from whoosh.analysis import StemmingAnalyzer


"""
cheeseburger_search.py 


Auth:

- this program uses google drive and therefore uses
  google's oauth mechanism to authenticate.
- gdrive_util.py takes care of creating the API instance
  from keys and creating an API service.



Flow:

program will:
   - create a Search object
   - call add_all_documents
   - calls open_index if no index exists
   - grab a list of repos
   - walk every issue
        - each issue body is (by itself) a document
        - each comment body is also a document
   - call add_document on each issue and each comment
   - add_document parses Markdown/adds docs to index following schema

program will occasionally:
   - ask to update the index
   - this opens the index, and adds all files in the path to a list
   - it then finds files that were deleted and files that were changed
   - it passes these to the indexer, then it's done

program calls the search function:
    - takes query from user
    - calls searcher.search(query, ...)
    - parses results from searcher into user-friendly search results
"""


class SearchResult:
    score = 1.0
    path = None
    content = ""
    content_highlight = ""
    headlines = None
    tags = ""


class DontEscapeHtmlInCodeRenderer(mistune.Renderer):
    def __init__(self, **kwargs):
        super(DontEscapeHtmlInCodeRenderer, self).__init__(**kwargs)

    def block_code(self, code, lang):
        if not lang:
            return '<pre><code>%s\n</code></pre>\n' % code
        return '<pre><code class="lang-%s">%s\n</code></pre>\n' % (lang, code)

    def codespan(self, text):
        return '<code>%s</code>' % text.rstrip()


class Search:
    ix = None
    index_folder = None
    markdown = mistune.Markdown(renderer=DontEscapeHtmlInCodeRenderer(), escape=False)
    html_parser = html.parser.HTMLParser()
    schema = None

    def __init__(self, index_folder):
        self.open_index(index_folder)

    def open_index(self, index_folder, create_new=False):
        """
        Create a schema,
        and create/open a search index
        that lives on disk.
        """
        self.index_folder = index_folder
        if create_new:
            if os.path.exists(index_folder):
                shutil.rmtree(index_folder)
                print("deleted index folder: " + index_folder)

        if not os.path.exists(index_folder):
            os.mkdir(index_folder)

        exists = index.exists_in(index_folder)
        stemming_analyzer = StemmingAnalyzer()

        # cheeseburger schema
        # useful:
        # https://developers.google.com/drive/api/v3/reference/files
        #
        # id -> id
        # url-> webViewLink
        # timestamp -> createdTime
        # owner -> owners[]['emailAddress']
        # owner_name -> owners[]['displayName']
        # title -> name
        # content -> (from pandoc)

        # IMPORTANT:
        # This is where the schema is defined.

        schema = Schema(
                id=ID(stored=True,unique=True),
                url=ID(stored=True, unique=True),
                mimetype=ID(stored=True),
                timestamp=ID(stored=True),
                owner_email=ID(stored=True),
                owner_name=ID(stored=True),
                title=TEXT(stored=True),
                content=TEXT(stored=True, analyzer=stemming_analyzer)
        )

        # Now that we have a schema,
        # make an index!
        if not exists:
            self.ix = index.create_in(index_folder, schema)
        else:
            self.ix = index.open_dir(index_folder)


    def update_index_incremental(self, 
                                 credentials_file, 
                                 config):
        """
        Update the index of issues of a given github repo.

        Takes as inputs:
        - github access token
        - list of github repos
        - github org/user owning these repos
        - location of the whoosh config file for configuring the search engine
        """

        # PoC||GTFO

        # Steps to rebuild all documents in index:
        # 
        # Step 1: walk each doc in google drive. 
        # Step 2: index it.
        # Step 2.5: deal with documents removed from google drive.
        # Step 3: grab a beer.

        # TODO:
        # Can make Step 2/2.5 shorter by storing hash of contents.
        # for now, just... uh... i dunno. 
        # figure it out later. don't remove.
        # update works exactly like add:
        # if a document already exists in the index,
        # it gets removed and re-added.

        ### if create_new_index:
        ###     self.open_index(self.index_folder, create_new=True)

        gd = GDrive()
        service = gd.get_service()

        # -----
        # Set of all documents on Google Drive:

        # Call the Drive v3 API

        results = service.files().list(
            pageSize=100, fields="nextPageToken, files(id, kind, mimeType, name, owners, webViewLink, createdTime)").execute()

        items = results.get('files', [])

        indexed_ids = set()
        for item in items:
            indexed_ids.add(item['id'])

        # TODO:
        # Tapping out at 100, use nextPageToken to get all later

        writer = self.ix.writer()

        temp_dir = tempfile.mkdtemp(dir=os.getcwd())
        print("Temporary directory: %s"%(temp_dir))
        if not os.path.exists(temp_dir):
            os.mkdir(temp_dir)

        count = 0
        for item in items:

            self.add_item(writer, item, indexed_ids, temp_dir, config)
            count += 1

        writer.commit()
        print("Done, updated %d documents in the index" % count)


    def add_item(self, writer, item, indexed_ids, temp_dir, config):
        """
        Add an item to the index.
        item is a google drive api document item.
        works like a dictionary.
        """
        # If we have already indexed this document, 
        # drop the old record first
        if item['id'] in indexed_ids:
            writer.delete_by_term('id',item['id'])

        gd = GDrive()
        service = gd.get_service()

        # IMPORTANT:
        # This is where the search documents are actually created.

        ##########################################
        # Two kinds of documents:
        # - documents with text that can be extracted and indexed
        # - every other kind
        #
        # In Google Drive land, that's (docx) and (everybody else).
        #
        # For each document living in the Google Drive folder,
        # - If mimeType is document:
        #   - Download it
        #   - Convert it to markdown
        #   - Extract and index the content
        #   - Index everything else
        # - Else:
        #   - Just index everything else


        mimetype = re.split('[/\.]',item['mimeType'])[-1]
        mimemap = {
                'document' : 'docx',
        }


        content = ""

        if(mimetype not in mimemap.keys()):

            # ----------
            # Not a document
            # 
            # No text to extract
            # 
            # Technically, there probably is,
            # but I'm not about to parse powerpoint
            # or mystery PDF files in python.

            print("Indexing document %s of type %s"%(item['name'], mimetype))

        else:

            # ----------
            # docx Content Extraction:
            # 
            # We can only do this with .docx files
            # This is a file type we know how to convert
            # Construct the URL and download it

            print("Extracting content from %s of type %s"%(item['name'], mimetype))


            # Create a URL and a destination filename
            file_ext = mimemap[mimetype]
            file_url = "https://docs.google.com/document/d/%s/export?format=%s"%(item['id'], file_ext)

            # This re could probablybe improved
            name = re.sub('/','_',item['name'])

            # Now make the pandoc input/output filenames
            out_ext = 'txt'
            pandoc_fmt = 'plain'
            if name.endswith(file_ext):
                infile_name = name
                outfile_name = re.sub(file_ext,out_ext,infile_name)
            else:
                infile_name  = name+'.'+file_ext
                outfile_name = name+'.'+out_ext


            # assemble input/output file paths
            fullpath_input = os.path.join(temp_dir,infile_name)
            fullpath_output = os.path.join(temp_dir,outfile_name)

            # Use requests.get to download url to file
            r = requests.get(file_url, allow_redirects=True)
            with open(fullpath_input, 'wb') as f:
                f.write(r.content)


            # Try to convert docx file to plain text
            try:
                output = pypandoc.convert_file(fullpath_input,
                                               pandoc_fmt,
                                               format='docx',
                                               outputfile=fullpath_output
                )
                assert output == ""
            except RuntimeError:
                print("XXXXXX Failed to index document %s"%(item['name']))


            # If export was successful, read contents of markdown
            # into the content variable.
            # into the content variable.
            if os.path.isfile(fullpath_output):
                # Export was successful
                with codecs.open(fullpath_output, encoding='utf-8') as f:
                    content = f.read()


            # No matter what happens, clean up.
            print("Cleaning up %s"%item['name'])

            subprocess.call(['rm','-fr',fullpath_output])
            #print(" ".join(['rm','-fr',fullpath_output]))

            subprocess.call(['rm','-fr',fullpath_input])
            #print(" ".join(['rm','-fr',fullpath_input]))


        mimetype = re.split('[/\.]', item['mimeType'])[-1]
        writer.add_document(
                id = item['id'],
                url = item['webViewLink'],
                mimetype = mimetype,
                timestamp = item['createdTime'],
                owner_email = item['owners'][0]['emailAddress'],
                owner_name = item['owners'][0]['displayName'],
                title = item['name'],
                content = content
        )


    def create_search_result(self, results):
        # Allow larger fragments
        results.fragmenter.maxchars = 300

        # Show more context before and after
        results.fragmenter.surround = 50

        search_results = []
        for r in results:

            # Note: this is where we package things up 
            # for the Jinja template "search.html".
            # For example, the Jinja template
            # contains a {% for e in entries %}
            # and then an {{e.score}}

            sr = SearchResult()
            sr.score = r.score


            # IMPORTANT:
            # update search.html with what you want to see
            # in each search result's "metadata" (links,
            # parent repos, users, etc.)

            # sr variables are available in Jinja
            # r variables are from documents (follow schema)

            sr.id = r['id']
            sr.url = r['url']
            sr.title = r['title']
            sr.mimetype = r['mimetype']

            sr.owner_email = r['owner_email']
            sr.owner_name = r['owner_name']

            sr.content = r['content']

            highlights = r.highlights('content')
            if not highlights:
                # just use the first 1,000 words of the document
                highlights = self.cap(r['content'], 1000)

            highlights = self.html_parser.unescape(highlights)
            html = self.markdown(highlights)
            sr.content_highlight = html

            search_results.append(sr)

        return search_results

    def cap(self, s, l):
        return s if len(s) <= l else s[0:l - 3] + '...'

    def search(self, query_list, fields=None):
        with self.ix.searcher() as searcher:
            query_string = " ".join(query_list)
            query = None
            if "\"" in query_string or ":" in query_string:
                query = QueryParser("content", self.schema).parse(query_string)
            elif len(fields) == 1 and fields[0] == "filename":
                pass
            elif len(fields) == 2:
                pass
            else:
                fields = ['id','url','timestamp','owner_email','owner_name','title','content'] 
            if not query:
                query = MultifieldParser(fields, schema=self.ix.schema).parse(query_string)
            parsed_query = "%s" % query
            print("query: %s" % parsed_query)
            results = searcher.search(query, terms=False, scored=True, groupedby="url")
            search_result = self.create_search_result(results)

        return parsed_query, search_result

    def get_document_total_count(self):
        return self.ix.searcher().doc_count_all()

if __name__ == "__main__":
    search = Search("search_index")
    search.add_all_documents("/Users/charles/codes/cheeseburger-search/config.py")

