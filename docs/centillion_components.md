# Centillion Components

Centillion keeps it simple.

There are two components:

* The `Search` object, which uses whoosh and various
  APIs (Github, Google Drive) to build and manage
  the search index. The `Search` object also runs all
  queries against the search index. (See the
  [Centillion Whoosh](centillion_whoosh.md) page
  or the `centillion_search`.py` file
  for details.)

* Flask app, which uses Jinja templates to present the
  user with a minimal web frontend that allows them
  to interact with the search engine. (See the
  [Centillion Flask](centillion_flask.md) page
  or the `centillion`.py` file
  for details.)


