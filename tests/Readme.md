# centillion tests

This directory contains tests for centillion,
the document search engine. This uses the
`unittest` library, and tests can be run
with `pytest`.

Tests will automatically load test configuration
files for centillion from the `tests/` directory.

We run the following tests:

* `test_routes.py` - create a centillion app with an
  empty search index, and test that each of the 
  routes created by the Flask app can be reached
  properly.

* `test_fakedocs.py` - create a centillion app,
  populate a search index with fake documents,
  and run tests of a centillion instance with
  documents in the search index.

* `test_gdrive.py` - requires `credentials.json` file
  containing Google Drive API credentials; create a
  centillion app and populate the search index with
  files from Google Drive.

* `test_gh.py` - requires Github API access token to
  be provided in conig file; create a centillion app,
  and popualte the search index with Github files,
  Markdown content, issues, and pull requests.

## Secrets for Travis

The strategy we use for getting API keys into Travis
to enable tests of centillion functionality using real
API calls is to tar anad encrypt all secret files.

The file `secrets.tar.gz.enc` is an encrypted file
that, when decrypted, contains a `secrets.tar.gz`
file with the files:

* `secrets.py` - contains API keys in varibles;
  imported/used by test configuration files

* `credentials.json` - contains Google Drive API
  credentials 

