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
  properly

* `test_fakedocs.py` - create a centillion app,
  populate a search index with fake documents,
  and run tests of a centillion instance with
  documents in the search index.

* `test_gh.py` - (requires Github API credentials 
  in environment variables) create a centillion app,
  populate a search index with issues and files from
  a small sample repo, and run tests of a centillion
  instance with documents.

