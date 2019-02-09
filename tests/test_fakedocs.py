import subprocess
import time
import os
import centillion
import unittest
from utils import SearchIndexException


"""
test_fakedocs

Populate a centillion search index instance
with fake documents, and run various tests
on a centillion instance with a populated 
search index.

To run, use pytest:

    $ pytest
    $ python -m unittest -q test_fakedocs.FakeDocsTest
"""


CONFIG_FILE = 'config_local_test.py'
INDEX_DIR = 'test_search_index'
HERE = os.path.split(os.path.abspath(__file__))[0]

# Search index directory location
si = os.path.join(HERE,INDEX_DIR)


class FakeDocsTest(unittest.TestCase):
    """
    Run tests on a centillion Flask app populated
    with fake documents.
    """
    @classmethod
    def setUpClass(self):
        """Set everything up for this test class
        """
        # Make sure no search index
        if os.path.exists(si):
            raise SearchIndexException("Error: no search index %s should exist, but one was found"%(si))

        # Create centillion and test client
        self.app = centillion.webapp.get_flask_app(config_file=os.path.join(HERE,CONFIG_FILE))

        # If we are running this test from
        # any directory other than tests/,
        # the search index will be built there.
        # (Typically this is the behavior we want.)
        # 
        # The following code forces the
        # search index to be built in the
        # tests/ directory.
        # (Desirable behavior for testing.)
        if os.path.abspath(os.getcwd()) != HERE:
            # we are not in tests/, use absolute path
            self.app.config['INDEX_DIR'] = si
        else:
            # we are in tests/, use relative path
            self.app.config['INDEX_DIR'] = INDEX_DIR

        self.client = self.app.test_client()


    @classmethod
    def tearDownClass(self):
        """Tear everything down when this test class is finished
        """
        # Clean up test search index directory
        if os.path.isdir(si):
            subprocess.call(['rm','-fr',si])

        # Make sure no search index
        if os.path.exists(si):
            raise SearchIndexException("Error: no search index %s should exist at end of test, but one was found"%(si))


    def test_1_update_index(self):
        """Test the update_index route for all document types
        """
        # Reindex the search index with fake docs
        r = self.client.get('/update_index/all')
        if r.status_code==302:
            r = self.client.get(r.headers['Location'])

        # If you don't insert a sleep right here,
        # the assert below runs before the document
        # is added to the search index.
        time.sleep(2)

        # Check that the search index exists
        if not os.path.exists(si):
            raise SearchIndexException("Error: search index %s should exist, but nothing was found"%(si))


    def test_2_document_counts(self):
        """Verify the document counts on the main index page
        """
        # Get index
        r = self.client.get('/')
        if r.status_code==302:
            r = self.client.get(r.headers['Location'])
        code = r.status_code
        data = str(r.data)
        self.assertIn('id="gdoc-count">2',data)
        self.assertIn('id="issue-count">1',data)
        self.assertIn('id="ghfile-count">1',data)
        self.assertIn('id="markdown-count">1',data)
        self.assertIn('id="disqus-count">1',data)


    def test_3_simple_search(self):
        """Verify that searches for known terms return expected results
        """
        # Create a map of search terms: (keys)
        # keys - the term to search for
        # values - list of strings that must appear in output
        simple_search = {
                'barley' : ['Disqus Thread','for the improvement thereof'],
                'masked+figure' : ['Google Drive File', 'Edgar Allen Poe'],
                'bananas' : ['Github File','preview','not available'],
                'bacteria' : ['Github Markdown','Github Issue','Chicken_and_Waffles.md','@pasteur','microbiologist Louis Pasteur'],
                'microscope' : ['Github Markdown','seventeenth century','Chicken_and_Waffles.md']
        }

        #'pineapple' : 'THIS IS BROKEN'
        #'oranges' : 'THIS IS BROKEN TOO'
        # need to index repo name too,
        # get partial matches on repo name
        # and on (full) file path

        for search_term in simple_search:

            r = self.client.get('/search?query=%s'%(search_term))
            code = r.status_code
            data = str(r.data)
            self.assertEqual(code,200)

            imperatives = simple_search[search_term]

            for imp in imperatives:
                self.assertIn(imp,data)

