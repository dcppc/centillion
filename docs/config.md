## Configuring centillion

centillion is configured using a single configuration file that contains
configuration details for both the flask frontend and the whoosh backend.

To pass a configuration file to centillion, use the `CENTILLION_CONFIG`
environment variable to specify the location of the configuration file 
when running the Python script that imports centillion and runs the 
webapp.

For example, an example Python script that runs centillion is provided
in `examples/run_centillion.py`. This script should be run as follows:

```bash
CENTILLION_CONFIG="conf/config_flask.py" python examples/run_centillion.py
```

An example centillion configuration file 

## Configuring API access

The centillion configuration file must contain API keys for each of the following
third-party services:

* Github 
* Groups.io
* Google Drive
* Disqus

#### Github

Two sets of Github API credentials are required.

**Access control layer:** The first set of Github API credentials 
are the credentials required to create the authentication layer
and verify that members trying to access centillion are members of
the correct Github organization. This takes the form of a client token
and a client secret.

**Search index layer:** The second set of Github API credentials are
the credentials used by centillion to access issues, pull requests,
and files in Github repositories. This takes the form of a single API
access token.

Github API credentials are provided in the configuration file.

See the example config file in the repo at `conf/config_flask.example.py`
for details.

#### Groups.io

The Groups.io API token is used to index email threads. This token must be
obtained using the Groups.io API.





