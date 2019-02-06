import subprocess
import os
import centillion
import unittest
from utils import SearchIndexException
from config_localtests import INDEX_DIR


"""
test_routes

Create an empty centillion instance and verify that
all Flask routes work as expected.

To run, use pytest:

    $ pytest
    $ python -m unittest -q test_routes.RoutesTest
"""


CONFIG_FILE = 'config_localtests.py'
INDEX_DIR = 'test_search_index'
HERE = os.path.split(os.path.abspath(__file__))[0]

# Search index directory location
si = os.path.join(HERE,INDEX_DIR)


class RoutesTest(unittest.TestCase):
    """
    Test all routes for a centillion instance
    with an empty search index.
    """
    @classmethod
    def setUpClass(self):
        """
        Set up for unit tests by creating a new centillion Flask app
        with our testing configuration file.
        """
        # Make sure no search index exists
        if os.path.exists(si):
            raise SearchIndexException("Error: no search index %s should exist, but one was found"%(si))

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
        del self.app
        del self.client

        # Clean up test search index directory
        if os.path.isdir(si):
            subprocess.call(['rm','-fr',si])

        # Make sure no search index
        if os.path.exists(si):
            raise SearchIndexException("Error: no search index %s should exist at end of test, but one was found"%(si))


    def test_routes_index(self):
        """Test Flask route /
        """
        r = self.client.get('/')
        if r.status_code==302:
            r = self.client.get(r.headers['Location'])

        code = r.status_code
        data = str(r.data)

        self.assertEqual(code,200)
        self.assertIn('Help using centillion',data)
        self.assertIn('centillion FAQ',data)
        self.assertIn('Google Drive files',data)
        self.assertIn('Github files',data)
        self.assertIn('Github issues',data)
        self.assertIn('Disqus comment',data)


    def test_routes_master_list(self):
        """Test Flask route /master_list
        """
        r = self.client.get('/master_list')
        if r.status_code==302:
            r = self.client.get(r.headers['Location'])

        code = r.status_code
        data = str(r.data)

        self.assertEqual(code,200)
        self.assertIn('Google Drive Files',data)
        self.assertIn('Github Files',data)
        self.assertIn('Github Issues',data)
        self.assertIn('Disqus Comment',data)


    def test_routes_control_panel(self):
        """Test Flask route /control_panel
        """
        r = self.client.get('/control_panel')
        if r.status_code==302:
            r = self.client.get(r.headers['Location'])

        code = r.status_code
        data = str(r.data)

        self.assertEqual(code,200)
        self.assertIn('Update Main Search Index',data)
        self.assertIn('Update Search Index by Type',data)


    def test_routes_help(self):
        """Test Flask route /help
        """
        r = self.client.get('/help')
        if r.status_code==302:
            r = self.client.get(r.headers['Location'])

        code = r.status_code
        data = str(r.data)

        self.assertEqual(code,200)
        self.assertIn('Help Page',data)


    def test_routes_faq(self):
        """Test Flask route /faq
        """
        r = self.client.get('/faq')
        if r.status_code==302:
            r = self.client.get(r.headers['Location'])

        code = r.status_code
        data = str(r.data)

        self.assertEqual(code,200)
        self.assertIn('FAQ Page',data)


