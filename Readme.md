# centillion

![version number](https://img.shields.io/badge/version-1.8public-blue.svg)

**centillion**: a document search engine that searches
across Github issues, Github pull requests, Github files,
Google Drive documents, Groups.io email threads, and
Disqus comment threads.

**a centillion**: a very large number consisting of a 1 with 303 zeros after it.

one centillion is 3.03 log-times better than a googol.

![Screen shot: centillion search](docs/images/search.png)


## What is centillion

centillion is a document search engine that can index different kinds of document
collections: Google Documents (.docx files), Google Drive files, Github issues,
Github files, Github Markdown files, and Groups.io email threads.


## How centillion works

We define the types of documents the centillion should index,
what information, and how. centillion then builds and
updates a search index.

centillion also provides a simple web frontend for running
queries against the search index. That's done using a Flask server.


## Quick start: using centillion

To use centillion, start with a Python script that will import
centillion, create an instance of the webapp, set any custom
configuration variables, and run the webapp. For example,
the following script is in `examples/run_centillion.py`:

```
import centillion

app = centillion.webapp.get_flask_app()

app.run()
```

When this script is run, centillion will also look for a configuration
file containing all of the keys and settings that centillion needs to run.
This can be provided using the `CENTILLION_CONFIG` variable:

```
CENTILLION_CONFIG="config/config_flask.py" python examples/run_centillion.py
```


## Resources for centillion

centillion repo on Github: <https://github.com/dcppc/centillion>

centillion documentation: <http://nih-data-commons.us/centillion>

