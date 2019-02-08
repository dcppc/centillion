from .const import base

from .gdrive_util import GDrive
from .disqus_util import DisqusCrawler

import os, re, io, requests
import os.path
import logging
import json

import dateutil.parser
import datetime
from dateutil.parser import parse

import bs4
import shutil
import pytz

from github import Github, GithubException
import base64

from apiclient.http import MediaIoBaseDownload

import mistune
from whoosh.fields import *
import whoosh.index as index
import tempfile, subprocess
import pypandoc
import codecs

from whoosh.query import Variations
from whoosh.qparser import MultifieldParser, QueryParser
from whoosh.analysis import StemmingAnalyzer, LowercaseFilter, StopFilter
from whoosh.qparser.dateparse import DateParserPlugin
from whoosh.qparser import GtLtPlugin
from whoosh import fields, index


"""
centillion_search.py 

Define a Search object for use by the centillion search engine.

Auth notes:
    - Google drive/Google oauth requires credentials.json
    - Github, Disqus require API tokens passed in 
      via centillion config file (available through Flask app.config)

Utility functions:
    - clean_timestamp (for cleanup of timestamps)
    - is_url (for cleanup of results)
    - SearchResult (simple class representing results)
    - DontEscapeHtmlInCodeRenderer (used to render markdown as html)

Search class:

    create:

    - open_index (create new schema, open index on disk)

    populate:

    - add_drive_file (add an individual google drive file item)
    - add_issue (add an individual github issue item)
    - add_ghfile (add an individual github file item)
    - add_disqusthread (add disqus comments thread)

    update:

    - update_index (update entire search index)
    - update_index_gdocs (iterate over all Google Drive documents and add them)
    - update_index_issues (iterate over all Github issues and add them)
    - update_index_ghfiles (iterate over all github files and add them)
    - update_index_disqus (iterate over all disqus comment threads and add them)

    test update:

    - test_update_index (called by update_index if testing)
    - test_update_index_gdocs (test harness for update_index_gdocs calls; if fake docs is enabled, this will populate index with fake docs)
    - test_update_index_issues (see above)
    - test_update_index_ghfiles (see above)
    - test_update_index_disqus (see above)

    search:

    - search (perform a search on the search index with the user's query)

    util:

    - create_search_results (package search results for the Flask template)
    - get_document_total_count (ask centillion for count of documents of each type)
    - get_list (get a listing of all files of a particular type)

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


here = os.path.abspath(os.path.dirname(__file__))


def clean_timestamp(dt):
    return dt.replace(microsecond=0).isoformat()

def is_url(u):
    if '...' in u:
        # special case of whoosh messing up urls
        return False
    if '<b' in u or '&lt;' in u:
        # special case of whoosh highlighting a word in a link
        return False
    if u[-1] is '-':
        # parsing error
        return False
    if u[0:2]=='ht' or u[0:2]=='ft' or u[0:2]=='//':
        return True
    return False

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
    schema = None

    def __init__(self, index_folder):
        self.open_index(index_folder)


    # ------------------------------
    # Update the entire index

    def update_index(self, gdrive_token_path, gh_token, disqus_token, run_which, config):
        """
        Update the entire search index
        """
        # Google Drive Files
        if run_which=='all' or run_which=='gdocs':
            if config['GOOGLE_DRIVE_ENABLED']:
                try:
                    self.update_index_gdocs(gdrive_token_path,config)
                except Exception as e:
                    msg = "ERROR: While re-indexing: failed to update Google Drive. Continuing..."
                    logging.exception(msg)
                    pass

        # Github files
        if run_which=='all' or run_which=='ghfiles':
            if config['GITHUB_ENABLED']:
                try:
                    self.update_index_ghfiles(gh_token,config)
                except Exception as e:
                    msg = "ERROR: While re-indexing: failed to update Github files. Continuing..."
                    logging.exception(msg)
                    pass

        # Github issues
        if run_which=='all' or run_which=='issues':
            if config['GITHUB_ENABLED']:
                try:
                    self.update_index_issues(gh_token,config)
                except Exception as e:
                    msg = "ERROR: While re-indexing: failed to update Github issues. Continuing..."
                    logging.exception(msg)
                    pass

        # Disqus
        if run_which=='all' or run_which=='disqus':
            if config['DISQUS_ENABLED']:
                try:
                    self.update_index_disqus(disqus_token, config)
                except Exception as e:
                    msg = "ERROR: While re-indexing: failed to update Disqus comment threads. Continuing..."
                    logging.exception(msg)
                    pass



    def test_update_index(self, run_which, config):
        """
        Update the search index with test docs
        for purposes of testing
        """
        # Google Drive Files
        if run_which=='all' or run_which=='gdocs':
            self.test_update_index_gdocs(config)

        # Github files
        if run_which=='all' or run_which=='ghfiles':
            self.test_update_index_ghfiles(config)

        # Github issues
        if run_which=='all' or run_which=='issues':
            self.test_update_index_issues(config)

        # Disqus
        if run_which=='all' or run_which=='disqus':
            self.test_update_index_disqus(config)


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
                msg = "Deleted index folder: " + index_folder
                logging.info(msg)

        if not os.path.exists(index_folder):
            os.mkdir(index_folder)

        exists = index.exists_in(index_folder)

        #stemming_analyzer = StemmingAnalyzer()
        stemming_analyzer = StemmingAnalyzer() | LowercaseFilter()
        #stemming_analyzer = StemmingAnalyzer() | LowercaseFilter() | StopFilter()

        
        # ------------------------------
        # This is where the search index's document schema
        # is defined.

        schema = Schema(
                id = fields.ID(stored=True, unique=True),
                kind = fields.ID(stored=True),

                created_time = fields.DATETIME(stored=True),
                modified_time = fields.DATETIME(stored=True),
                indexed_time = fields.DATETIME(stored=True),
                
                title = fields.TEXT(stored=True, field_boost=100.0),

                url = fields.ID(stored=True),
                
                mimetype = fields.TEXT(stored=True),

                owner_email = fields.ID(stored=True),
                owner_name = fields.TEXT(stored=True),

                # mainly for email threads
                group = fields.ID(stored=True),

                repo_name = fields.TEXT(stored=True),
                repo_url = fields.ID(stored=True),
                github_user = fields.TEXT(stored=True),

                tags = fields.KEYWORD(commas=True,
                                      stored=True,
                                      lowercase=True),

                # comments only
                issue_title = fields.TEXT(stored=True, field_boost=100.0),
                issue_url = fields.ID(stored=True),

                content = fields.TEXT(stored=True, analyzer=stemming_analyzer)
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
            msg = "Indexing Google Drive file \"%s\" of type %s"%(item['name'], mimetype)
            logging.info(msg)

            writer.delete_by_term('id',item['id'])

            # Index a plain google drive file
            created_time = dateutil.parser.parse(item['createdTime'])
            modified_time = dateutil.parser.parse(item['modifiedTime'])
            indexed_time = datetime.datetime.now().replace(microsecond=0)
            try:
                writer.add_document(
                        id = item['id'],
                        kind = 'gdoc',
                        created_time = created_time,
                        modified_time = modified_time,
                        indexed_time = indexed_time,
                        title = item['name'],
                        url = item['webViewLink'],
                        mimetype = mimetype,
                        owner_email = item['owners'][0]['emailAddress'],
                        owner_name = item['owners'][0]['displayName'],
                        group='',
                        repo_name='',
                        repo_url='',
                        github_user='',
                        issue_title='',
                        issue_url='',
                        content = content
                )
            except ValueError:
                err = " > XXXXXX Failed to index Google Drive file \"%s\""%(item['name'])
                logging.exception(err)

        else:
            # Document with text
            # Perform content extraction

            # -----------
            # docx Content Extraction:
            # 
            # We can only do this with .docx files
            # This is a file type we know how to convert
            # Construct the URL and download it

            msg = "Indexing Google Drive document \"%s\" of type %s"%(item['name'], mimetype)
            logging.info(msg)

            logging.info(" > Extracting content")


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
                err = " > XXXXXX Failed to index Google Drive document \"%s\""%(item['name'])
                logging.exception(err)


            # If export was successful, read contents of markdown
            # into the content variable.
            if os.path.isfile(fullpath_output):
                # Export was successful
                with codecs.open(fullpath_output, encoding='utf-8') as f:
                    content = f.read()


            # No matter what happens, clean up.
            msg = " > Cleaning up \"%s\""%item['name']
            logging.info(msg)

            ## test
            msg = " ".join(['rm','-fr',fullpath_output])
            logging.info(msg)

            msg = " ".join(['rm','-fr',fullpath_input])
            logging.info(msg)

            # do it
            subprocess.call(['rm','-fr',fullpath_output])
            subprocess.call(['rm','-fr',fullpath_input])

            if update:
                logging.info(" > Removing old record")
                writer.delete_by_term('id',item['id'])
            else:
                logging.info(" > Creating a new record")

            try:
                created_time = dateutil.parser.parse(item['createdTime'])
                modified_time = dateutil.parser.parse(item['modifiedTime'])
                indexed_time = datetime.datetime.now()
                writer.add_document(
                        id = item['id'],
                        kind = 'gdoc',
                        created_time = created_time,
                        modified_time = modified_time,
                        indexed_time = indexed_time,
                        title = item['name'],
                        url = item['webViewLink'],
                        mimetype = mimetype,
                        owner_email = item['owners'][0]['emailAddress'],
                        owner_name = item['owners'][0]['displayName'],
                        group='',
                        repo_name='',
                        repo_url='',
                        github_user='',
                        issue_title='',
                        issue_url='',
                        content = content
                )
            except ValueError:
                msg = " > XXXXXX Failed to index Google Drive file \"%s\""%(item['name'])
                logging.exception(msg)




    # ------------------------------
    # Add a single github issue and its comments
    # to a search index.


    def add_issue(self, writer, issue, gh_token, config, update=True):
        """
        Add a Github issue/comment to a search index.
        """
        repo = issue.repository
        repo_name = repo.owner.login+"/"+repo.name
        repo_url = repo.html_url

        msg = "Indexing issue %s"%(issue.html_url)
        logging.info(msg)
        
        if issue is None:
            err = "ERROR: Github issue passed to add_issue() was None!"
            logging.exception(err)
            raise Exception(err)

        if issue.body is None:
            err = "ERROR: Github issue passed to add_issue() has no body! "
            err += "(continuing anyway...)"
            logging.exception(err)
            #raise Exception(err)

        # Combine comments with their respective issues.
        # Otherwise just too noisy.
        try:
            issue_comment_content = issue.body.rstrip()
        except AttributeError:
            issue_comment_content = ""
        issue_comment_content += "\n"

        # Handle the comments content
        if(issue.comments>0):

            try:
                comments = issue.get_comments()
                for comment in comments:

                    try:
                        issue_comment_content += comment.body.rstrip()
                    except AttributeError:
                        pass
                    issue_comment_content += "\n"

            except GithubException:
                err = "ERROR: could not get comments for this issue: %s"
                logging.exception(err)
                pass

        # Now create the actual search index record.
        # Add one document per issue thread,
        # containing entire text of thread.

        created_time = issue.created_at
        modified_time = issue.updated_at
        indexed_time = datetime.datetime.now()
        try:
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
                    group='',
                    repo_name = repo_name,
                    repo_url = repo_url,
                    github_user = issue.user.login,
                    issue_title = issue.title,
                    issue_url = issue.html_url,
                    content = issue_comment_content
            )
        except ValueError:
            err = "ERROR: Failed to index Github issue \"%s\""%(issue.title)
            logging.exception(err)



    # ------------------------------
    # Add a single github file 
    # to a search index.

    def add_ghfile(self, writer, d, gh_token, config, update=True):
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
            logging.exception("ERROR: Failed to find file info.")
            logging.error(d.keys())
            return


        indexed_time = datetime.datetime.now()

        if fext in MARKDOWN_EXTS:
            msg = "Indexing markdown doc %s from repo %s"%(fname,repo_name)
            logging.info(msg)

            # Unpack the requests response and decode the content
            # 
            # don't forget the headers for private repos!
            # useful: https://bit.ly/2LSAflS

            headers = {'Authorization' : 'token %s'%(gh_token)}

            response = requests.get(furl, headers=headers)
            if response.status_code==200:
                jresponse = response.json()
                content = ""
                try:
                    binary_content = re.sub('\n','',jresponse['content'])
                    content = base64.b64decode(binary_content).decode('utf-8')
                except KeyError:
                    err = "ERROR: Failed to extract 'content' field. You probably hit the rate limit."
                    logging.exception(err)
                    return 

            else:
                err = "ERROR: Failed to reach file URL. There may be a problem with authentication/headers."
                logging.error(err)
                return 

            usable_url = "https://github.com/%s/blob/master/%s"%(repo_name, fpath)

            # Now create the actual search index record
            try:
                writer.add_document(
                        id = fsha,
                        kind = 'markdown',
                        created_time = None,
                        modified_time = None,
                        indexed_time = indexed_time,
                        title = fname,
                        url = usable_url,
                        mimetype='',
                        owner_email='',
                        owner_name='',
                        group='',
                        repo_name = repo_name,
                        repo_url = repo_url,
                        github_user = '',
                        issue_title = '',
                        issue_url = '',
                        content = content
                )
            except ValueError as e:
                err = "ERROR: Failed to index Github markdown file \"%s\""%(fname)
                logging.exception(err)
                return 


        else:
            msg = "Indexing github file %s from repo %s"%(fname,repo_name)
            logging.info(msg)

            key = fname+"_"+fsha

            if d['type'] == 'blob':
                usable_url = "https://github.com/%s/blob/master/%s"%(repo_name, fpath)

            elif d['type'] == 'tree':
                usable_url = "https://github.com/%s/tree/master/%s"%(repo_name, fpath)

            else:
                usable_url = repo_url

            # Now create the actual search index record
            try:
                writer.add_document(
                        id = key,
                        kind = 'ghfile',
                        created_time = None,
                        modified_time = None,
                        indexed_time = indexed_time,
                        title = fname,
                        url = usable_url,
                        mimetype='',
                        owner_email='',
                        owner_name='',
                        group='',
                        repo_name = repo_name,
                        repo_url = repo_url,
                        github_user = '',
                        issue_title = '',
                        issue_url = '',
                        content = ''
                )
            except ValueError as e:
                err = "ERROR: Failed to index Github file \"%s\""%(fname)
                logging.exception(err)



    # ------------------------------
    # Add a single disqus comment thread
    # to the search index.

    def add_disqusthread(self, writer, d, config, update=True):
        """
        Use a disqus comment thread record
        to add a disqus comment thread to the
        search index.
        """
        indexed_time = datetime.datetime.now()

        # created_time is already a timestamp

        # Now create the actual search index record
        try:
            writer.add_document(
                    id = d['id'],
                    kind = 'disqus',
                    created_time = d['created_time'],
                    modified_time = None,
                    indexed_time = indexed_time,
                    title = d['title'],
                    url = d['link'],
                    mimetype='',
                    owner_email='',
                    owner_name='',
                    repo_name = '',
                    repo_url = '',
                    github_user = '',
                    issue_title = '',
                    issue_url = '',
                    content = d['content']
            )
        except ValueError as e:
            err = "ERROR: Failed to index Disqus comment thread \"%s\""%(d['title'])
            logging.exception(err)




    # ------------------------------
    # Define how to update search index
    # using different kinds of collections


    # ------------------------------
    # Google Drive Files/Documents


    def update_index_gdocs(self, gdrive_token_path, config):
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
        # - drop all indexed ids
        # - index all remote ids


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
        gd = GDrive(gdrive_token_path,config)
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
            
            if nextPageToken is None or config['TRUNCATE_DRIVE_LISTING'] is True:
                # stop if we are finished or if the 
                # user has asked to truncate the 
                # drive files list
                break


        writer = self.ix.writer()
        count = 0
        temp_dir = tempfile.mkdtemp(dir=os.getcwd())

        err = "centillion.search: Update Google Docs search index: using temporary directory: %s"%(temp_dir)
        logging.info(err)

        try:

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

        except Exception as e:
            err = "ERROR: Could not add Google Drive files to search index. Continuing..."
            logging.exception(err)
            pass

        msg = "centillion.search: Cleaning temporary directory: %s"%(temp_dir)
        logging.info(msg)
        subprocess.call(['rm','-fr',temp_dir])

        writer.commit()

        msg = "centillion.search: Done, updated %d Google Drive files in the index" % count
        logging.info(msg)


    def test_update_index_gdocs(self, config):
        """
        Update the search index using fake
        Google document item.
        """
        p = QueryParser("kind", schema=self.ix.schema)

        writer = self.ix.writer()

        # Clear out the fake docs if they
        # already exist in the search index
        q = p.parse("gdoc")
        with self.ix.searcher() as s:
            results = s.search(q,limit=None)
            indexed_ids = set()
            for result in results:
                indexed_ids.add(result['id'])
            for drop_id in indexed_ids:
                writer.delete_by_term('id',drop_id)

        # Load the fakes

        # google drive document (full content)
        with open(os.path.join(here,'payloads/gdoc_sample.json'),'r') as f:
            sample = json.load(f)

        for k in ['indexed_time','created_time','modified_time']:
            sample[k] = parse(sample[k])

        # Write it to the search index
        writer.add_document(**sample)

        # google drive file (no content)
        with open(os.path.join(here,'payloads/gdrive_sample.json'),'r') as f:
            sample2 = json.load(f)

        for k in ['indexed_time','created_time','modified_time']:
            sample2[k] = parse(sample2[k])

        # Write it to the search index
        writer.add_document(**sample2)

        writer.commit()

        msg = "Done, updated 2 fake Google Drive documents in the index"
        logging.info(msg)



    # ------------------------------
    # Github Issues/Comments

    def update_index_issues(self, gh_token, config):
        """
        Update the search index using a collection of 
        Github repo issues and comments.
        """
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
        g = Github(gh_token)

        # Now index all issue threads in the user-specified repos

        # Start by collecting all the things
        remote_issues = set()
        full_items = {}

        # Iterate over each repo 
        list_of_repos = config['REPOSITORIES']
        for k, r in enumerate(list_of_repos):

            if '/' not in r:
                err = "Error: specify org/reponame or user/reponame in list of repos"
                logging.error(err)
                raise Exception(err)

            this_org, this_repo = re.split('/',r)
            try:
                org = g.get_organization(this_org)
                repo = org.get_repo(this_repo)
            except:
                try:
                    user = g.get_user(this_org) 
                    repo = user.get_repo(this_repo)
                except:
                    err = "ERROR: could not gain access to repository %s"%(r)
                    logging.error(err)
                    continue

            # Iterate over each issue thread
            open_issues   = repo.get_issues(state='open')
            closed_issues = repo.get_issues(state='closed')

            for j, issue in enumerate(open_issues):
                # For each issue/comment URL,
                # grab the key and store the 
                # corresponding issue object
                key = issue.html_url
                value = issue
                remote_issues.add(key)
                full_items[key] = value

            for j, issue in enumerate(closed_issues):
                key = issue.html_url
                value = issue
                remote_issues.add(key)
                full_items[key] = value

            # Stop early if testing
            if config['TRUNCATE_ISSUES_LISTING'] is True and k>=1:
                break


        writer = self.ix.writer()
        count = 0

        # Drop issues in indexed_issues
        for drop_issue in indexed_issues:
            writer.delete_by_term('id',drop_issue)


        # Add any issue in remote_issues
        for add_issue in remote_issues:
            item = full_items[add_issue]
            self.add_issue(writer, item, gh_token, config, update=False)
            count += 1


        writer.commit()

        msg = "Done, updated %d Github issues in the index" % count
        logging.info(msg)


    def test_update_index_issues(self, config):
        """
        Update the search index using fake
        Github issue.
        """
        p = QueryParser("kind", schema=self.ix.schema)

        writer = self.ix.writer()

        # Clear out the fake docs if they
        # already exist in the search index
        q = p.parse("issue")
        with self.ix.searcher() as s:
            results = s.search(q,limit=None)
            indexed_ids = set()
            for result in results:
                indexed_ids.add(result['id'])
            for drop_id in indexed_ids:
                writer.delete_by_term('id',drop_id)

        # Load the fake
        with open(os.path.join(here,'payloads/ghissue_sample.json'),'r') as f:
            sample = json.load(f)

        for k in ['indexed_time','created_time','modified_time']:
            sample[k] = parse(sample[k])

        # Write it to the search index
        writer.add_document(**sample)
        writer.commit()

        msg = "Done, updated 1 fake Github issue in the index"
        logging.info(msg)



    # ------------------------------
    # Github Files

    def update_index_ghfiles(self, gh_token, config): 
        """
        Update the search index using a collection of 
        files (and, separately, Markdown files) from 
        a Github repo.
        """
        # Get the set of indexed ids:
        # ------
        indexed_ids = set()
        p = QueryParser("kind", schema=self.ix.schema)
        q = p.parse("ghfile")
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
        g = Github(gh_token)

        # Now index all the files.

        # Start by collecting all the things
        remote_ids = set()
        full_items = {}

        # Iterate over each repo 
        list_of_repos = config['REPOSITORIES']
        for j, r in enumerate(list_of_repos):

            if '/' not in r:
                err = "ERROR: specify org/reponame or user/reponame in list of repos"
                logging.error(err)
                raise Exception(err)

            this_org, this_repo = re.split('/',r)
            try:
                org = g.get_organization(this_org)
                repo = org.get_repo(this_repo)
            except:
                try:
                    user = g.get_user(this_org) 
                    repo = user.get_repo(this_repo)
                except:
                    err = "ERROR: could not gain access to repository %s"%(r)
                    logging.exception(err)
                    continue


            # Get head commit
            commits = repo.get_commits()
            try:
                last = commits[0]
                sha = last.sha
            except GithubException:
                err = "ERROR: could not get commits from repository %s"%(r)
                logging.exception(err)
                continue

            # Get all the docs
            tree = repo.get_git_tree(sha=sha, recursive=True)
            docs = tree.raw_data['tree']
            msg = "Parsing file ids from repository %s"%(r)
            logging.info(msg)

            for d in docs:

                # For each doc, get the file extension
                # and decide what to do with it.

                fpath = d['path']
                _, fname = os.path.split(fpath)
                _, fext = os.path.splitext(fpath)
                fpathpieces = fpath.split('/')

                # Ignore anything whose name starts with . or _
                ignore_file = fname[0]=='.' or fname[0]=='_'
                ignore_dir = False
                for piece in fpathpieces:
                    if piece[0]=='.' or piece[0]=='_':
                        ignore_dir = True

                if not ignore_file and not ignore_dir:
                    key = d['sha']

                    d['org'] = this_org
                    d['repo'] = this_repo
                    value = d

                    remote_ids.add(key)
                    full_items[key] = value

            # TESTING should end early (after 3 repos)
            if config['TESTING'] is True and j>3:
                break

        writer = self.ix.writer()
        count = 0

        # Drop any id in indexed_ids
        for drop_id in indexed_ids:
            writer.delete_by_term('id',drop_id)

        # Add any issue in remote_ids
        # and in remote_ids
        for add_id in remote_ids:
            item = full_items[add_id]
            self.add_ghfile(writer, item, gh_token, config, update=False)
            count += 1

        writer.commit()

        msg = "Done, updated %d Github files in the index" % count
        logging.info(msg)


    def test_update_index_ghfiles(self, config):
        """
        Update the search index using fake
        Github file.
        """
        p = QueryParser("kind", schema=self.ix.schema)

        writer = self.ix.writer()

        # Clear out the fake docs if they
        # already exist in the search index
        for doctype in ["ghfile","markdown"]:
            q = p.parse(doctype)
            with self.ix.searcher() as s:
                results = s.search(q,limit=None)
                indexed_ids = set()
                for result in results:
                    indexed_ids.add(result['id'])
                for drop_id in indexed_ids:
                    writer.delete_by_term('id',drop_id)

        # Load the fakes
        with open(os.path.join(here,'payloads/ghfile_sample.json'),'r') as f:
            filesample = json.load(f)

        for k in ['indexed_time','created_time','modified_time']:
            try:
                filesample[k] = parse(filesample[k])
            except:
                filesample[k] = None

        with open(os.path.join(here,'payloads/ghmd_sample.json'),'r') as f:
            mdsample = json.load(f)

        for k in ['indexed_time','created_time','modified_time']:
            try:
                mdsample[k] = parse(mdsample[k])
            except:
                mdsample[k] = None

        # Write them to the search index
        writer.add_document(**filesample)
        writer.add_document(**mdsample)
        writer.commit()

        msg = "Done, updated 1 fake Github file and 1 fake Github markdown file in the index"
        logging.info(msg)


    
    # ------------------------------
    # Disqus Threads


    def update_index_disqus(self, disqus_token, config):
        """
        Update the search index using a collection of 
        Disqus comment threads from the dcppc-internal 
        forum.
        """
        # Updated algorithm:
        # - get set of indexed ids
        # - get set of remote ids
        # - drop all indexed ids
        # - index all remote ids

        # Get the set of indexed ids:
        # --------------------
        indexed_ids = set()
        p = QueryParser("kind", schema=self.ix.schema)
        q = p.parse("disqus")
        with self.ix.searcher() as s:
            results = s.search(q,limit=None)
            for result in results:
                indexed_ids.add(result['id'])

        # Get the set of remote ids:
        # ------
        spider = DisqusCrawler(disqus_token,'dcppc-internal')

        # ask spider to crawl disqus comments
        spider.crawl_threads()

        # spider.comments will be a dictionary
        # with keys as thread IDs and values as
        # a dictionary item

        writer = self.ix.writer()
        count = 0

        # archives is a dictionary
        # keys are IDs (urls)
        # values are dictionaries
        threads = spider.get_threads()

        # Start by collecting all the things
        remote_ids = set()
        for k in threads.keys():
            remote_ids.add(k)

        # drop indexed_ids
        for drop_id in indexed_ids:
            writer.delete_by_term('id',drop_id)

        # add remote_ids
        for add_id in remote_ids:
            item = threads[add_id]
            self.add_disqusthread(writer, item, config, update=False)
            count += 1

        writer.commit()

        msg = "Done, updated %d Disqus comment threads in the index" % count
        logging.info(msg)


    def test_update_index_disqus(self, config):    
        """
        Update the search index using fake
        Disqus comment threads.
        """
        p = QueryParser("kind", schema=self.ix.schema)

        writer = self.ix.writer()

        # Clear out the fake docs if they
        # already exist in the search index
        q = p.parse("disqus")
        with self.ix.searcher() as s:
            results = s.search(q,limit=None)
            indexed_ids = set()
            for result in results:
                indexed_ids.add(result['id'])
            for drop_id in indexed_ids:
                writer.delete_by_term('id',drop_id)

        # Load the fake
        with open(os.path.join(here,'payloads/disqus_sample.json'),'r') as f:
            sample = json.load(f)

        for k in ['indexed_time','created_time','modified_time']:
            try:
                sample[k] = parse(sample[k])
            except:
                sample[k] = None

        # Write it to the search index
        writer.add_document(**sample)
        writer.commit()

        msg = "Done, updated 1 fake Disqus comment thread in the index"
        logging.info(msg)




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

            try:
                sr.created_time =  datetime.datetime.strftime(r['created_time'],  "%Y-%m-%d %I:%M %p")
            except KeyError:
                sr.created_time = ''

            try:
                sr.modified_time = datetime.datetime.strftime(r['modified_time'], "%Y-%m-%d %I:%M %p")
            except KeyError:
                sr.modified_time = ''

            try:
                sr.indexed_time =  datetime.datetime.strftime(r['indexed_time'],  "%Y-%m-%d %I:%M %p")
            except KeyError:
                sr.indexed_time = ''

            sr.title = r['title']
            sr.url = r['url']

            sr.mimetype = r['mimetype']

            try:
                sr.owner_email = r['owner_email']
            except KeyError:
                sr.owner_email = ''

            try:
                sr.owner_name = r['owner_name']
            except KeyError:
                sr.owner_name = ''

            try:
                sr.group = r['group']
            except KeyError:
                sr.group = ''

            try:
                sr.repo_name = r['repo_name']
                sr.repo_url = r['repo_url']
            except KeyError:
                sr.repo_name = ''
                sr.repo_url = ''

            try:
                sr.issue_title = r['issue_title']
                sr.issue_url = r['issue_url']
            except:
                sr.issue_title = ''
                sr.issue_url = ''

            try:
                sr.github_user = r['github_user']
            except:
                sr.github_user = ''

            sr.content = r['content']

            # This is where we need to fix the markdown rendering problems

            highlights = r.highlights('content')
            if not highlights:
                # just use the first 1,000 words of the document
                highlights = self.cap(r['content'], 1000)

            import html
            highlights = html.unescape(highlights)

            # ----------------------------------------------
            # Before continuing, we need to process some of the
            # search results to address problems.

            # Look for markdown links following the pattern [link text](link url)
            resrch = re.search('\[(.*)\]\((.*)\)',highlights)
            if resrch is not None:
                # Extract the link url and check if it looks like a URL
                u = resrch.groups()[1]
                if not is_url(u):
                    # This is a relative Markdown link, so we need to break it
                    # by putting a space between [link text] and (link url)
                    new_highlights = re.sub('\[(.*)\]\((.*)\)','[\g<1>] (\g<2>)',highlights)
                    highlights = new_highlights

            # If we have any <table> tags in our search results,
            # we make a BeautifulSoup from the results, which will
            # fill in all missing/unpaired tags, then extract the 
            # text from the soup.
            if '<table>' in highlights:
                soup = bs4.BeautifulSoup(highlights,features="html.parser")
                highlights = soup.text
                del soup

            # Okay, back to the show.
            # ----------------------------------------------

            html = self.markdown(highlights)
            html = re.sub(r'\n','<br />',html)

            # Scrub broken links
            soup = bs4.BeautifulSoup(html,features="html.parser")
            for tag in soup.find_all('a'):
                u = tag.get('href')
                if not is_url(u):
                    tag.replaceWith(tag.text)

            result = str(soup)
            result = re.sub('\] \(','](',result)
            sr.content_highlight = result

            search_results.append(sr)

        return search_results




    def cap(self, s, l):
        return s if len(s) <= l else s[0:l - 3] + '...'

    def get_document_total_count(self):
        p = QueryParser("kind", schema=self.ix.schema)

        counts = {
                "gdoc" : None,
                "issue" : None,
                "ghfile" : None,
                "markdown" : None,
                "disqus" : None,
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
            item_keys = ['title','owner_name','url','mimetype','created_time','modified_time']
        elif doctype=='issue':
            item_keys = ['title','repo_name','repo_url','url','created_time','modified_time']
        elif doctype=='disqus':
            item_keys = ['title','created_time','url']
        elif doctype=='ghfile':
            item_keys = ['title','repo_name','repo_url','url']
        elif doctype=='markdown':
            item_keys = ['title','repo_name','repo_url','url']
        else:
            err = "Could not find document of type %s"%(doctype)
            logging.exception(err)
            raise Exception(err)

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



    def search(self, query_list, fields=None):

        with self.ix.searcher() as searcher:

            query_list2 = []
            for qq in query_list:
                if qq=='AND' or qq=='OR':
                    query_list2.append(qq)
                else:
                    query_list2.append(qq.lower())
            query_string = " ".join(query_list2)

            query = None
            if ":" in query_string:
                # If the user DOES specify a field,
                # setting the fields determines what fields
                # are searched with the free terms (no field)
                fields = ['title', 'content','owner_name','owner_email','github_user']
                query = MultifieldParser(fields, schema=self.ix.schema)
                est = pytz.timezone('America/New_York')
                query.add_plugin(DateParserPlugin(free=True, basedate=est.localize(datetime.datetime.utcnow())))
                query.add_plugin(GtLtPlugin())
                try:
                    query = query.parse(query_string)
                except:
                    # Because the DateParser plugin is an idiot
                    query_string2 = re.sub(r':(\w+)',':\'\g<1>\'',query_string)
                    try:
                        query = query.parse(query_string2)
                    except:
                        msg = "parsing query %s failed"%(query_string)
                        msg += "\n"
                        msg += "parsing query %s also failed"%(query_string2)
                        logging.exception(msg)
                        query = query.parse('')

            else:
                # If the user does not specify a field,
                # these are the fields that are actually searched
                fields = ['url','title', 'content','owner_name','owner_email','github_user']
                query = MultifieldParser(fields, schema=self.ix.schema)
                est = pytz.timezone('America/New_York')
                query.add_plugin(DateParserPlugin(free=True, basedate=est.localize(datetime.datetime.utcnow())))
                query.add_plugin(GtLtPlugin())
                try:
                    query = query.parse(query_string)
                except:
                    err = "parsing query %s failed"%(query_string)
                    logging.exception(err)
                    query = query.parse('')
            parsed_query = "%s" % query
            msg = "query: %s" % parsed_query
            logging.info(msg)
            results = searcher.search(query, terms=False, scored=True, groupedby="kind")
            search_result = self.create_search_result(results)

        return parsed_query, search_result


