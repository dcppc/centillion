import shutil
import html.parser

from github import Github

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
from datetime import datetime

from whoosh.qparser import MultifieldParser, QueryParser
from whoosh.analysis import StemmingAnalyzer


"""
centillion_search.py 

Define a Search object for use by the centillion search engine.

Auth:
- google drive/google oauth requires credentials.json
- github oauth requires api token passed via GITHUB_TOKEN

Search object functions:
- open_index - creates the schema
- add_issue
- add_document - 2 methods with diff sigs
- update_index_issues
- update_index_gdocs - 2 methods to update respective collections
- update_main_index - update entire search index (calls update_index_*)
- create_search_results - package things up for jinja
- search - run the query, pass results to jinja-packager

Schema:
    - id
    - kind
    - created_time
    - modified_time
    - indexed_time
    - title
    - url
    - mimetype
    - owner_email
    - owner_name
    - repo_name
    - repo_url
    - issue_title
    - issue_url
    - github_user
    - content
"""


def clean_timestamp(dt):
    return dt.replace(microsecond=0).isoformat()


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

        
        # ------------------------------
        # IMPORTANT:
        # This is where the search index's document schema
        # is defined.

        schema = Schema(
                id = ID(stored=True, unique=True),
                kind = ID(stored=True),

                created_time = ID(stored=True),
                modified_time = ID(stored=True),
                indexed_time = ID(stored=True),
                
                title = TEXT(stored=True, field_boost=100.0),
                url = ID(stored=True, unique=True),
                
                mimetype=ID(stored=True),
                owner_email=ID(stored=True),
                owner_name=TEXT(stored=True),
                
                repo_name=TEXT(stored=True),
                repo_url=ID(stored=True),

                github_user=TEXT(stored=True),

                # comments only
                issue_title=TEXT(stored=True, field_boost=100.0),
                issue_url=ID(stored=True),
                
                content=TEXT(stored=True, analyzer=stemming_analyzer)
        )


        # Now that we have a schema,
        # make an index!
        if not exists:
            self.ix = index.create_in(index_folder, schema)
        else:
            self.ix = index.open_dir(index_folder)


    # ------------------------------
    # IMPORTANT:
    # Define how to add documents


    def add_drive_file(self, writer, item, indexed_ids, temp_dir, config):
        """
        Add a Google Drive document/file to a search index.
        If it is a document, extract the contents.
        """
        gd = GDrive()
        service = gd.get_service()

        # ------------------------
        # Two kinds of documents:
        # - documents with text that can be extracted (docx)
        # - everything else

        mimetype = re.split('[/\.]',item['mimeType'])[-1]
        mimemap = {
                'document' : 'docx',
        }

        content = ""
        if(mimetype not in mimemap.keys()):
            # Not a document - 
            # Just a file
            print("Indexing document \"%s\" of type %s"%(item['name'], mimetype))
        else:
            # Document with text
            # Perform content extraction

            # -----------
            # docx Content Extraction:
            # 
            # We can only do this with .docx files
            # This is a file type we know how to convert
            # Construct the URL and download it

            print("Extracting content from \"%s\" of type %s"%(item['name'], mimetype))


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
                print("XXXXXX Failed to index document \"%s\""%(item['name']))


            # If export was successful, read contents of markdown
            # into the content variable.
            # into the content variable.
            if os.path.isfile(fullpath_output):
                # Export was successful
                with codecs.open(fullpath_output, encoding='utf-8') as f:
                    content = f.read()


            # No matter what happens, clean up.
            print("Cleaning up \"%s\""%item['name'])

            subprocess.call(['rm','-fr',fullpath_output])
            #print(" ".join(['rm','-fr',fullpath_output]))

            subprocess.call(['rm','-fr',fullpath_input])
            #print(" ".join(['rm','-fr',fullpath_input]))


        # ------------------------------
        # IMPORTANT:
        # This is where the search documents are actually created.

        print("ok we are in add_document territory")
        mimetype = re.split('[/\.]', item['mimeType'])[-1]
        writer.add_document(
                id = item['id'],
                kind = 'gdoc',
                created_time = item['createdTime'],
                modified_time = item['modifiedTime'],
                indexed_time = datetime.now().replace(microsecond=0).isoformat(),
                title = item['name'],
                url = item['webViewLink'],
                mimetype = mimetype,
                owner_email = item['owners'][0]['emailAddress'],
                owner_name = item['owners'][0]['displayName'],
                repo_name='',
                repo_url='',
                github_user='',
                issue_title='',
                issue_url='',
                content = content
        )


    def add_issue(self, writer, issue, repo, config):
        """
        Add a Github issue/comment to a search index.
        """
        repo_name = repo.owner.name+"/"+repo.name
        repo_url = repo.html_url

        count = 0


        # Handle the issue content
        print("Indexing issue %s"%(issue.html_url))

        created_time = clean_timestamp(issue.created_at)
        modified_time = clean_timestamp(issue.updated_at)
        indexed_time = clean_timestamp(datetime.now())

        writer.add_document(
                id = issue.html_url,
                kind = 'issue',
                created_time = created_time,
                modified_time = modified_time,
                indexed_time = indexed_time,
                title = issue.title,
                url = issue.html_url,
                mimetype='',
                owner_email='',
                owner_name='',
                repo_name = repo_name,
                repo_url = repo_url,
                github_user = issue.user.login,
                issue_title = issue.title,
                issue_url = issue.html_url,
                content = issue.body.rstrip()
        )
        count += 1



        # Handle the comments content
        if(issue.comments>0):

            comments = issue.get_comments()
            for comment in comments:

                print(" > Indexing comment %s"%(comment.html_url))

                created_time = clean_timestamp(comment.created_at)
                modified_time = clean_timestamp(comment.updated_at)
                indexed_time = clean_timestamp(datetime.now())

                writer.add_document(
                        id = comment.html_url,
                        kind = 'comment',
                        created_time = created_time,
                        modified_time = modified_time,
                        indexed_time = indexed_time,
                        title = "Comment on "+issue.title,
                        url = comment.html_url,
                        mimetype='',
                        owner_email='',
                        owner_name='',
                        repo_name = repo_name,
                        repo_url = repo_url,
                        github_user = comment.user.login,
                        issue_title = issue.title,
                        issue_url = issue.html_url,
                        content = comment.body.rstrip()
                )

        count += 1
        return count



    # ------------------------------
    # Define how to update search index
    # using different kinds of collections

    def update_index_gdocs(self, 
                           config):
        """
        Update the search index using a collection of 
        Google Drive documents and files.
        """
        gd = GDrive()
        service = gd.get_service()

        # -----
        # Get the set of all documents on Google Drive:

        # ------------------------------
        # IMPORTANT:
        # This determines what information about the Google Drive files
        # you'll get back, and that's all you're going to have to work with.
        # If you need more information, modify the statement below.
        # Also see:
        # https://developers.google.com/drive/api/v3/reference/files

        gd = GDrive()
        service = gd.get_service()
        drive = service.files()


        # The trick is to set next page token to None 1st time thru (fencepost)
        nextPageToken = None

        # Use the pager to return all the things
        items = []
        while True:
            ps = 12
            results = drive.list(
                    pageSize=ps,
                    pageToken=nextPageToken,
                    fields="nextPageToken, files(id, kind, createdTime, modifiedTime, mimeType, name, owners, webViewLink)",
                    spaces="drive"
            ).execute()

            nextPageToken = results.get("nextPageToken")
            items += results.get("files", [])
            
            # Keep it short
            break

            #if nextPageToken is None:
            #    break

        indexed_ids = set()
        for item in items:
            indexed_ids.add(item['id'])

        writer = self.ix.writer()

        temp_dir = tempfile.mkdtemp(dir=os.getcwd())
        print("Temporary directory: %s"%(temp_dir))
        if not os.path.exists(temp_dir):
            os.mkdir(temp_dir)

        count = 0
        for item in items:
            self.add_drive_file(writer, item, indexed_ids, temp_dir, config)
            count += 1

        writer.commit()
        print("Done, updated %d documents in the index" % count)




    def update_index_issues(self, 
                            gh_access_token,
                            config):
        """
        Update the search index using a collection of 
        Github repo issues and comments.
        """
        # Strategy:
        # To get the proof of concept up and running,
        # we are just deleting and re-indexing every issue/comment.

        g = Github(gh_access_token)

        # Set of all URLs as existing on github
        to_index = set()

        writer = self.ix.writer()

        # Iterate over each repo
        list_of_repos = config['repositories']
        for r in list_of_repos:

            if '/' not in r:
                err = "Error: specify org/reponame or user/reponame in list of repos"
                raise Exception(err)

            this_org, this_repo = re.split('/',r)

            org = g.get_organization(this_org)
            repo = org.get_repo(this_repo)

            count = 0

            # Iterate over each thread
            issues = repo.get_issues()
            for issue in issues:

                # This approach is more work than is needed
                # but PoC||GTFO

                # For each issue/comment URL,
                # remove the corresponding item
                # and re-add it to the index

                to_index.add(issue.html_url)
                writer.delete_by_term('url', issue.html_url)
                count -= 1
                comments = issue.get_comments()

                for comment in comments:
                    to_index.add(comment.html_url)
                    writer.delete_by_term('url', comment.html_url)

                # Now re-add this issue to the index
                # (this will also add the comments)
                count += self.add_issue(writer, issue, repo, config)


        writer.commit()
        print("Done, updated %d documents in the index" % count)


    # ---------------------------------
    # Search results bundler


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
            sr.kind = r['kind']

            sr.created_time = r['created_time']
            sr.modified_time = r['modified_time']
            sr.indexed_time = r['indexed_time']

            sr.title = r['title']
            sr.url = r['url']

            sr.mimetype = r['mimetype']

            sr.owner_email = r['owner_email']
            sr.owner_name = r['owner_name']

            sr.repo_name = r['repo_name']
            sr.repo_url = r['repo_url']

            sr.issue_title = r['issue_title']
            sr.issue_url = r['issue_url']

            sr.github_user = r['github_user']

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

        # ------------------
        # github issues
        # create search results





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
                # If the user does not specify a field,
                # these are the fields that are actually searched
                fields = ['title',
                          'content']
            if not query:
                query = MultifieldParser(fields, schema=self.ix.schema).parse(query_string)
            parsed_query = "%s" % query
            print("query: %s" % parsed_query)
            results = searcher.search(query, terms=False, scored=True, groupedby="kind")
            search_result = self.create_search_result(results)

        return parsed_query, search_result



    def cap(self, s, l):
        return s if len(s) <= l else s[0:l - 3] + '...'

    def get_document_total_count(self):
        p = QueryParser("kind", schema=self.ix.schema)

        kind_labels = {
                "Documents" : "gdoc",
                "Issues" :    "issue",
                "Comments" :  "comment"
        }
        counts = {
                "Documents" : None,
                "Issues" : None,
                "Comments" : None,
                "Total" : None
        }
        for key in kind_labels:
            kind = kind_labels[key]
            q = p.parse(kind)
            with self.ix.searcher() as s:
                results = s.search(q,limit=None)
                counts[key] = len(results)

        counts['Total'] = self.ix.searcher().doc_count_all()

        return counts

if __name__ == "__main__":
    search = Search("search_index")

    from get_centillion_config import get_centillion_config
    config = get_centillion_config('config_centillion.json')

    gh_token = os.environ['GITHUB_TOKEN']

    search.update_index_issues(gh_token,config)
    search.update_index_gdocs(config)

