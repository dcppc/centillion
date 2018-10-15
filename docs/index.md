# centillion

![version number](https://img.shields.io/badge/version-1.7-blue.svg)

<https://search.nihdatacommons.us/>

**centillion**: a search engine that searches across Github issues, Github pull requests, Github files, 
Google Drive documents, Groups.io email threads, and Disqus comment threads.

**a centillion**: a very large number consisting of a 1 with 303 zeros after it.

one centillion is 3.03 log-times better than a googol.

![Screen shot: centillion search](docs/images/search.png)


## What is centillion

centillion (<https://search.nihdatacommons.us> is a search engine that can index 
different kinds of document collections: Google Documents (.docx files), Google Drive files,
Github issues, Github files, Github Markdown files, and Groups.io email threads.


## How centillion works

We define the types of documents the centillion should index,
what info and how. centillion then builds and
updates a search index. That's all done in `centillion_search.py`.

centillion also provides a simple web frontend for running
queries against the search index. That's done using a Flask server
defined in `centillion.py`.

centillion keeps it simple.


## Quick start: using centillion

Also see [Quick Start](quickstart.md).

To use centillion, start with a Python script that will import
centillion, create an instance of the webapp, set any custom
configuration variables, and run the webapp. For example,
the following script is in `examples/run_centillion.py`:

```python
import centillion

app = centillion.webapp.get_flask_app()

app.config['foo'] = 'bar'

app.run()
```

When this script is run, centillion will also look for a configuration
file containing all of the keys and settings that centillion needs to run.
This can be provided using the `CENTILLION_CONFIG` variable:

```bash
CENTILLION_CONFIG="conf/config_flask.py" python examples/run_centillion.py
```

## Submodules 

See [Submodules of centillion](submodules.md) page for details
about how centillion is organized into submodules.

