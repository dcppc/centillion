# centillion

![version number](https://img.shields.io/badge/version-1.8public-blue.svg)

**centillion**: a search engine that searches across Github issues, Github pull requests, Github files, 
Google Drive documents, Groups.io email threads, and Disqus comment threads.

**a centillion**: a very large number consisting of a 1 with 303 zeros after it.

One centillion is 3.03 log-times better than a googol.

![Screenshot: centillion search](images/search.png)


## What is centillion

centillion is a search engine that can index different kinds of document
collections: Google Documents (.docx files), Google Drive files, Github issues,
Github files, Github Markdown files, and Groups.io email threads.


## How centillion works

The backend of centillion defines how documents are obtained and how
the search index is constructed. centillion builds and updates the
search index by using APIs to get the latest versions of documents,
and updates its search index accordingly. ([More information](backend.md))

The centillion frontend provides a web interface for running queries
and interfacing with the search index. ([More information](frontend.md))


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


## Configuring centillion

See the [Configuring centillion](config.md) page for more information
about the centillion configuration file, what information is provided,
and how to point centillion to the configuration file.


## Submodules 

See the [Submodules of centillion](submodules.md) page for details
about how centillion is organized into submodules.

The search functionality is implemented in centillion's 
[backend `search` submodule](backend.md). This uses the
Whoosh library in Python.

The web interface is implemented in centillion's
[frontend `webapp` submodule](frontend.md). This implements
a web interface for centillion using the Flask library in 
Python.

To restrict access to centillion, we implement an OAuth
application that verifies users are members of a particular 
Github organization. See [Github authentication layer](auth.md)
for details.


## APIs

See the [APIs](api_all.md) page for an overview of the third-party
APIs that centillion interfaces with to populate the search index.

