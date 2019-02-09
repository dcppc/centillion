centillion is configured using a single configuration file that contains
configuration details for both the flask frontend and the whoosh backend.

## General Info

## Example config files

## Test config files







## Just one configuration file (frontend+backend)

To configure centillion, provide a single configuration file that 
specifies configuration details for both the Flask webapp frontend
and the search backend.

There is an example configuration file in 
the repository at:

```
config/config_flask.example.py
```

The contents of this file are given below:

```
# github oauth (access control)
GITHUB_OAUTH_CLIENT_ID = "XXX"
GITHUB_OAUTH_CLIENT_SECRET = "YYY"

# github acces token (issues/PRs/files)
GITHUB_TOKEN = "XXX"

# groups.io
GROUPSIO_TOKEN = "XXXXX"

# disqus 
DISQUS_TOKEN = "XXXXX"

# location of search index on disk
INDEX_DIR = "search_index"

# labels for repo footer
FOOTER_REPO_ORG = "dcppc"
FOOTER_REPO_NAME = "centillion"

# Flask secret key
SECRET_KEY = 'XXXXX'

REPOSITORIES = [
        "dcppc/organize",
        "dcppc/apis",
        "dcppc/data-stewards",
        ...
]
```

## Pass location with environment variable

The location of this configuration file should be passed in to the program
running centillion via the `CENTILLION_CONFIG` environment variable. For 
example, if the program `examples/run_centillion.py` contains a script that
imports centillion and runs the webapp, you can pass the config file using the
`CENTILLION_CONFIG` environment variable like this:

```
CENTILLION_CONFIG="config/config_flask.py" python examples/run_centillion.py
```

## Configuring API access

The centillion configuration file must contain API keys for each of the following
third-party services:

* Github 
* Groups.io
* Google Drive
* Disqus

See [APIs](apis_all.md) page for details about the types of API keys
required and how each API is used by centillion.

