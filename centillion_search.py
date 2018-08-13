import shutil
import html.parser

from github import Github, GithubException
import base64

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
    - fingerprint
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


    # ------------------------------
    # Create a schema and open a search index
    # on disk.

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
        # This is where the search index's document schema
        # is defined.

        schema = Schema(
                id = ID(stored=True, unique=True),
                kind = ID(stored=True),
                #fingerprint = ID(stored=True),

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


    def add_drive_file(self, writer, item, temp_dir, config, update=False):
        """
        Add a Google Drive document/file to a search index.
        If it is a document, extract the contents.
        """

        # There are two kinds of documents:
        # - documents with text that can be extracted (docx)
        # - everything else
        
        mimetype = re.split('[/\.]',item['mimeType'])[-1]
        mimemap = {
                'document' : 'docx',
        }

        content = ""
        if mimetype not in mimemap.keys():

            # Not a document - just a file
            print("Indexing Google Drive file \"%s\" of type %s"%(item['name'], mimetype))
            writer.delete_by_term('id',item['id'])

            # Index a plain google drive file
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


        else:
            # Document with text
            # Perform content extraction

            # -----------
            # docx Content Extraction:
            # 
            # We can only do this with .docx files
            # This is a file type we know how to convert
            # Construct the URL and download it

            print("Indexing Google Drive document \"%s\" of type %s"%(item['name'], mimetype))
            print(" > Extracting content")


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


            # Assemble input/output file paths
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
                print(" > XXXXXX Failed to index document \"%s\""%(item['name']))


            # If export was successful, read contents of markdown
            # into the content variable.
            if os.path.isfile(fullpath_output):
                # Export was successful
                with codecs.open(fullpath_output, encoding='utf-8') as f:
                    content = f.read()


            # No matter what happens, clean up.
            print(" > Cleaning up \"%s\""%item['name'])

            ## test
            #print(" ".join(['rm','-fr',fullpath_output]))
            #print(" ".join(['rm','-fr',fullpath_input]))

            # do it
            subprocess.call(['rm','-fr',fullpath_output])
            subprocess.call(['rm','-fr',fullpath_input])

            if update:
                print(" > Removing old record")
                writer.delete_by_term('id',item['id'])
            else:
                print(" > Creating a new record")

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




    # ------------------------------
    # Add a single github issue and its comments
    # to a search index.


    def add_issue(self, writer, issue, gh_access_token, config, update=True):
        """
        Add a Github issue/comment to a search index.
        """
        repo = issue.repository
        repo_name = repo.owner.login+"/"+repo.name
        repo_url = repo.html_url

        print("Indexing issue %s"%(issue.html_url))

        # Combine comments with their respective issues.
        # Otherwise just too noisy.
        issue_comment_content = issue.body.rstrip()
        issue_comment_content += "\n"

        # Handle the comments content
        if(issue.comments>0):

            comments = issue.get_comments()
            for comment in comments:

                issue_comment_content += comment.body.rstrip()
                issue_comment_content += "\n"

        # Now create the actual search index record
        created_time = clean_timestamp(issue.created_at)
        modified_time = clean_timestamp(issue.updated_at)
        indexed_time = clean_timestamp(datetime.now())

        # Add one document per issue thread,
        # containing entire text of thread.
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
                content = issue_comment_content
        )




    def add_ghfile(self, writer, d, gh_access_token, config, update=True):
        """
        Use a Github file API record to add a filename
        to the search index.
        """
        MARKDOWN_EXTS = ['.md','.markdown']

        repo = d['repo']
        org = d['org']
        repo_name = org + "/" + repo
        repo_url = "https://github.com/" + repo_name

        try:
            fpath = d['path']
            furl = d['url']
            fsha = d['sha']
            _, fname = os.path.split(fpath)
            _, fext = os.path.splitext(fpath)
        except:
            print(" > XXXXXXXX Failed to find file info.")
            return

        indexed_time = clean_timestamp(datetime.now())

        if fext in MARKDOWN_EXTS:
            print("Indexing markdown doc %s from repo %s"%(fname,repo_name))

            # Unpack the requests response and decode the content
            # 
            # don't forget the headers for private repos!
            # useful: https://bit.ly/2LSAflS

            headers = {'Authorization' : 'token %s'%(gh_access_token)}

            response = requests.get(furl, headers=headers)
            if response.status_code==200:
                jresponse = response.json()
                content = ""
                try:
                    binary_content = re.sub('\n','',jresponse['content'])
                    content = base64.b64decode(binary_content).decode('utf-8')
                except KeyError:
                    print(" > XXXXXXXX Failed to extract 'content' field. You probably hit the rate limit.")

            else:
                print(" > XXXXXXXX Failed to reach file URL. There may be a problem with authentication/headers.")
                return 

            usable_url = "https://github.com/%s/blob/master/%s"%(repo_name, fpath)

            # Now create the actual search index record
            writer.add_document(
                    id = fsha,
                    kind = 'markdown',
                    created_time = '',
                    modified_time = '',
                    indexed_time = indexed_time,
                    title = fname,
                    url = usable_url,
                    mimetype='',
                    owner_email='',
                    owner_name='',
                    repo_name = repo_name,
                    repo_url = repo_url,
                    github_user = '',
                    issue_title = '',
                    issue_url = '',
                    content = content
            )

        else:
            print("Indexing github file %s from repo %s"%(fname,repo_name))

            key = fname+"_"+fsha

            # Now create the actual search index record
            writer.add_document(
                    id = key,
                    kind = 'ghfile',
                    created_time = '',
                    modified_time = '',
                    indexed_time = indexed_time,
                    title = fname,
                    url = repo_url,
                    mimetype='',
                    owner_email='',
                    owner_name='',
                    repo_name = repo_name,
                    repo_url = repo_url,
                    github_user = '',
                    issue_title = '',
                    issue_url = '',
                    content = ''
            )



    # ------------------------------
    # Define how to update search index
    # using different kinds of collections


    # ------------------------------
    # Google Drive Files/Documents

    def update_index_gdocs(self, 
                           config):
        """
        Update the search index using a collection of 
        Google Drive documents and files.
        
        Uses the 'id' field to uniquely identify documents.

        Also see:
        https://developers.google.com/drive/api/v3/reference/files
        """

        # Updated algorithm:
        # - get set of indexed ids
        # - get set of remote ids
        # - drop indexed ids not in remote ids
        # - index all remote ids
        # - add hash check in add_


        # Get the set of indexed ids:
        # ------
        indexed_ids = set()
        p = QueryParser("kind", schema=self.ix.schema)
        q = p.parse("gdoc")
        with self.ix.searcher() as s:
            results = s.search(q,limit=None)
            for result in results:
                indexed_ids.add(result['id'])


        # Get the set of remote ids:
        # ------
        # Start with google drive api object
        gd = GDrive()
        service = gd.get_service()
        drive = service.files()

        # Now index all the docs in the google drive folder

        # The trick is to set next page token to None 1st time thru (fencepost)
        nextPageToken = None

        # Use the pager to return all the things
        remote_ids = set()
        full_items = {}
        while True:
            ps = 100
            results = drive.list(
                    pageSize=ps,
                    pageToken=nextPageToken,
                    fields = "nextPageToken, files(id, kind, createdTime, modifiedTime, mimeType, name, owners, webViewLink)",
                    spaces="drive"
            ).execute()

            nextPageToken = results.get("nextPageToken")
            files = results.get("files",[])
            for f in files:
                
                # Add all remote docs to a set
                remote_ids.add(f['id'])

                # Also store the doc
                full_items[f['id']] = f
            
            ## Shorter:
            #break
            # Longer:
            if nextPageToken is None:
                break


        writer = self.ix.writer()
        count = 0
        temp_dir = tempfile.mkdtemp(dir=os.getcwd())
        print("Temporary directory: %s"%(temp_dir))



        # Drop any id in indexed_ids
        # not in remote_ids
        drop_ids = indexed_ids - remote_ids
        for drop_id in drop_ids:
            writer.delete_by_term('id',drop_id)


        # Update any id in indexed_ids
        # and in remote_ids
        update_ids = indexed_ids & remote_ids
        for update_id in update_ids:
            # cop out
            writer.delete_by_term('id',update_id)
            item = full_items[update_id]
            self.add_drive_file(writer, item, temp_dir, config, update=True)
            count += 1


        # Add any id not in indexed_ids
        # and in remote_ids
        add_ids = remote_ids - indexed_ids
        for add_id in add_ids:
            item = full_items[add_id]
            self.add_drive_file(writer, item, temp_dir, config, update=False)
            count += 1


        print("Cleaning temporary directory: %s"%(temp_dir))
        subprocess.call(['rm','-fr',temp_dir])

        writer.commit()
        print("Done, updated %d documents in the index" % count)


    # ------------------------------
    # Github Issues/Comments

    def update_index_issues(self, gh_access_token, config):
        """
        Update the search index using a collection of 
        Github repo issues and comments.
        """
        # Updated algorithm:
        # - get set of indexed ids
        # - get set of remote ids
        # - drop indexed ids not in remote ids
        # - index all remote ids

        # Get the set of indexed ids:
        # ------
        indexed_issues = set()
        p = QueryParser("kind", schema=self.ix.schema)
        q = p.parse("issue")
        with self.ix.searcher() as s:
            results = s.search(q,limit=None)
            for result in results:
                indexed_issues.add(result['id'])


        # Get the set of remote ids:
        # ------
        # Start with api object
        g = Github(gh_access_token)

        # Now index all issue threads in the user-specified repos

        # Start by collecting all the things
        remote_issues = set()
        full_items = {}

        # Iterate over each repo 
        list_of_repos = config['repositories']
        for r in list_of_repos:

            if '/' not in r:
                err = "Error: specify org/reponame or user/reponame in list of repos"
                raise Exception(err)

            this_org, this_repo = re.split('/',r)
            try:
                org = g.get_organization(this_org)
                repo = org.get_repo(this_repo)
            except:
                print("Error: could not gain access to repository %s"%(r))
                continue

            # Iterate over each issue thread
            issues = repo.get_issues()
            for issue in issues:

                # For each issue/comment URL,
                # grab the key and store the 
                # corresponding issue object
                key = issue.html_url
                value = issue

                remote_issues.add(key)
                full_items[key] = value

        writer = self.ix.writer()
        count = 0

        # Drop any issues in indexed_issues
        # not in remote_issues
        drop_issues = indexed_issues - remote_issues
        for drop_issue in drop_issues:
            writer.delete_by_term('id',drop_issue)


        # Update any issue in indexed_issues
        # and in remote_issues
        update_issues = indexed_issues & remote_issues
        for update_issue in update_issues:
            # cop out
            writer.delete_by_term('id',update_issue)
            item = full_items[update_issue]
            self.add_issue(writer, item, gh_access_token, config, update=True)
            count += 1


        # Add any issue not in indexed_issues
        # and in remote_issues
        add_issues = remote_issues - indexed_issues
        for add_issue in add_issues:
            item = full_items[add_issue]
            self.add_issue(writer, item, gh_access_token, config, update=False)
            count += 1


        writer.commit()
        print("Done, updated %d documents in the index" % count)



    # ------------------------------
    # Github Markdown Files

    def update_index_ghfiles(self, gh_access_token, config): 
        """
        Update the search index using a collection of 
        files (and, separately, Markdown files) from 
        a Github repo.
        """
        # Updated algorithm:
        # - get set of indexed ids
        # - get set of remote ids
        # - drop indexed ids not in remote ids
        # - index all remote ids

        # Get the set of indexed ids:
        # ------
        indexed_ids = set()
        p = QueryParser("kind", schema=self.ix.schema)
        q = p.parse("ghfiles")
        with self.ix.searcher() as s:
            results = s.search(q,limit=None)
            for result in results:
                indexed_ids.add(result['id'])

        q = p.parse("markdown")
        with self.ix.searcher() as s:
            results = s.search(q,limit=None)
            for result in results:
                indexed_ids.add(result['id'])

        # Get the set of remote ids:
        # ------
        # Start with api object
        g = Github(gh_access_token)

        # Now index all the files.

        # Start by collecting all the things
        remote_ids = set()
        full_items = {}

        # Iterate over each repo 
        list_of_repos = config['repositories']
        for r in list_of_repos:

            if '/' not in r:
                err = "Error: specify org/reponame or user/reponame in list of repos"
                raise Exception(err)

            this_org, this_repo = re.split('/',r)
            try:
                org = g.get_organization(this_org)
                repo = org.get_repo(this_repo)
            except:
                print("Error: could not gain access to repository %s"%(r))
                continue


            # Get head commit
            commits = repo.get_commits()
            try:
                last = commits[0]
                sha = last.sha
            except GithubException:
                print("Error: could not get commits from repository %s"%(r))
                continue

            # Get all the docs
            tree = repo.get_git_tree(sha=sha, recursive=True)
            docs = tree.raw_data['tree']
            print("Parsing file ids from repository %s"%(r))

            for d in docs:

                # For each doc, get the file extension
                # and decide what to do with it.

                fpath = d['path']
                _, fname = os.path.split(fpath)
                _, fext = os.path.splitext(fpath)

                key = d['sha']

                d['org'] = this_org
                d['repo'] = this_repo
                value = d

                remote_ids.add(key)
                full_items[key] = value

        writer = self.ix.writer()
        count = 0

        # Drop any id in indexed_ids
        # not in remote_ids
        drop_ids = indexed_ids - remote_ids
        for drop_id in drop_ids:
            writer.delete_by_term('id',drop_id)


        # Update any id in indexed_ids
        # and in remote_ids
        update_ids = indexed_ids & remote_ids
        for update_id in update_ids:
            # cop out: just delete and re-add
            writer.delete_by_term('id',update_id)
            item = full_items[update_id]
            self.add_ghfile(writer, item, gh_access_token, config, update=True)
            count += 1


        # Add any issue not in indexed_ids
        # and in remote_ids
        add_ids = remote_ids - indexed_ids
        for add_id in add_ids:
            item = full_items[add_id]
            self.add_ghfile(writer, item, gh_access_token, config, update=False)
            count += 1


        writer.commit()
        print("Done, updated %d Github files in the index" % count)



    # ------------------------------
    # Groups.io Emails


    #def update_index_markdown(self, gh_access_token, config): 





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
            html = re.sub(r'\n','<br />',html)
            sr.content_highlight = html

            search_results.append(sr)

        return search_results




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

        counts = {
                "gdoc" : None,
                "issue" : None,
                "ghfile" : None,
                "markdown" : None,
                "total" : None
        }
        for key in counts.keys():
            q = p.parse(key)
            with self.ix.searcher() as s:
                results = s.search(q,limit=None)
                counts[key] = len(results)

        counts['total'] = sum(counts[k] for k in counts.keys())

        return counts


    def get_list(self,doctype):
        """
        Get a listing of all files, 
        so we can construct the page that 
        lists everyone and everything that
        centillion indexes.
        """
        # Unfortunately, we have to treat
        # each doctype separately, b/c of
        # what is most relevant to display
        # in the everything-list.
        item_keys=''
        if doctype=='gdoc':
            item_keys = ['title','owner_name','url','mimetype']
        elif doctype=='issue':
            item_keys = ['title','repo_name','repo_url','url']
        elif doctype=='ghfile':
            item_keys = ['title','repo_name','repo_url','url']
        elif doctype=='markdown':
            item_keys = ['title','repo_name','repo_url','url']
        else:
            raise Exception("Could not find document of type %s"%(doctype))

        json_results = []

        p = QueryParser("kind", schema=self.ix.schema)
        q = p.parse(doctype)
        with self.ix.searcher() as s:
            results = s.search(q,limit=None)
            for r in results:
                d = {}
                for k in item_keys:
                    d[k] = r[k]
                json_results.append(d)

        return json_results


if __name__ == "__main__":
    search = Search("search_index")

    from get_centillion_config import get_centillion_config
    config = get_centillion_config('config_centillion.json')

    gh_token = os.environ['GITHUB_TOKEN']

    search.update_index_issues(gh_token,config)
    search.update_index_gdocs(config)

