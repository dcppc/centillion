import subprocess
import time
import os
import centillion
import unittest
import pytest
from utils import SearchIndexException


"""
test_gh

Test a real centillion instance hooked up to 
a real Github account and making real
calls to the Github API. 

To run, use pytest:

    $ pytest
    $ py.test -q -s test_gh.py::GithubTest
"""


CONFIG_FILE = 'config_gh.py'
INDEX_DIR = 'test_search_index_gh'
HERE = os.path.split(os.path.abspath(__file__))[0]

# Search index directory location
si = os.path.join(HERE,INDEX_DIR)


class GithubTest(unittest.TestCase):
    """
    Run tests on a centillion Flask app
    with real Github API credentials.
    """
    @classmethod
    def setUpClass(self):
        """
        These steps are carried out before 
        the tests in this class.
        """
        # Make sure no search index
        if os.path.exists(si):
            raise SearchIndexException("Error: no search index %s should exist, but one was found"%(si))

        # Create centillion and test client
        self.app = centillion.webapp.get_flask_app(config_file=os.path.join(HERE,CONFIG_FILE))

        # Build search index in the tests/ dir
        if os.path.abspath(os.getcwd()) != HERE:
            # not in tests/
            self.app.config['INDEX_DIR'] = si
        else:
            # in tests/
            self.app.config['INDEX_DIR'] = INDEX_DIR

        self.client = self.app.test_client()

        self.update_index_all()

    @classmethod
    def tearDownClass(self):
        """
        These steps are carried out after 
        all tests finish. 
        """
        # Clean up test search index directory
        if os.path.isdir(si):
            subprocess.call(['rm','-fr',si])

        # Make sure no search index
        if os.path.exists(si):
            raise SearchIndexException("Error: no search index %s should exist at end of test, but one was found"%(si))

        del self.app
        del self.client


    @classmethod
    def update_index_all(self):
        """Reindex the search index with (real) docs
        """
        r = self.client.get('/update_index/all')
        if r.status_code==302:
            r = self.client.get(r.headers['Location'])

        time.sleep(2)


    def test_1_searchindex(self):
        """Check to make sure search index exists
        """
        # Check that the search index exists
        if not os.path.exists(si):
            raise SearchIndexException("Error: search index %s should exist, but nothing was found"%(si))


    @pytest.mark.flaky(reruns=5, reruns_delay=10)
    def test_2_document_counts(self):
        """
        Verify document counts for this real
        Google Drive folder/example.
        """
        # Get index
        r = self.client.get('/')
        if r.status_code==302:
            r = self.client.get(r.headers['Location'])
        code = r.status_code
        data = str(r.data)

        # should find 1 issue + 1 pull request
        self.assertIn('id="issue-count">2',data)

        # should find 2 files, 1 markdown
        self.assertIn('id="ghfile-count">2',data)
        self.assertIn('id="markdown-count">1',data)


    @pytest.mark.flaky(reruns=5, reruns_delay=10)
    def test_3_simple_search(self):
        """
        Verify that searches for known terms 
        will return expected results
        """
        simple_search = {
                'laser+sharks' : ['Github Markdown','Readme.md'],
                'tarantula' : ['Github Issue','Add a license to this repository'],
                'seattle' : ['Github Issue','@charlesreid1','Range Rover']
        }

        for search_term in simple_search:

            r = self.client.get('/search?query=%s'%(search_term))
            code = r.status_code
            data = str(r.data)
            self.assertEqual(code,200)

            imperatives = simple_search[search_term]

            for imp in imperatives:
                self.assertIn(imp,data)

