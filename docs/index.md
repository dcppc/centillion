# Centillion

**centillion**: a pan-github-markdown-issues-google-docs search engine.

**a centillion**: a very large number consisting of a 1 with 303 zeros after it.

centillion is 3.03 log-times better than the googol.

## What is centillion

Centillion is a search engine built using [whoosh](https://whoosh.readthedocs.io/en/latest/intro.html),
a Python library for building search engines.


We define the types of documents centillion should index,
what info and how. Centillion then builds and
updates a search index. That's all done in `centillion_search.py`.

Centillion also provides a simple web frontend for running
queries against the search index. That's done using a Flask server
defined in `centillion.py`.

Centillion keeps it simple.


## Quickstart

Run centillion with a github access token API key set via
environment variable:

```
GITHUB_TOKEN="XXXXXXXX" python centillion.py
```

This will start a Flask server, and you can view the minimal search engine
interface in your browser at <http://localhost:5000>.

## Configuration

### Centillion configuration

`config_centillion.json` defines configuration variables
for centillion - namely, what to index, and how, and where.

### Flask configuration

`config_flask.py` defines configuration variables
used by flask, which controls the web frontend 
for centillion.

## Control Panel/Rebuilding Search Index

To rebuild the search engine, visit the control panel route (`/control_panel`),
for example at <http://localhost:5000/control_panel>.

This allows you to rebuild the search engine index. The search index
is stored in the `search_index/` directory, and that directory
can be configured with centillion's configuration file.

The diff search index is faster to build, as it only
indexes documents that have been added since the last
new document was added to the search index.

The main search index is slower to build, as it will
re-index everything.

(Cron scripts? Threaded task that runs hourly?)

## Details

More on the details of how centillion works.

Under the hood, centillion uses flask and whoosh.
Flask builds and runs the web server.
Whoosh handles search requests and management
of the search index.

[Centillion Components](centillion_components.md)

[Centillion Flask](centillion_flask.md)

[Centillion Whoosh](centillion_whoosh.md)


