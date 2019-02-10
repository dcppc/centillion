The configuration file is the main way to customize
the behavior of the centillion application.

To specify a configuration file, use the `config_file`
keyword when calling `centillion.webapp.get_flask_app()`:

```
import centillion
app = centillion.webapp.get_flask_app(config_file='../config/config_centillion_fakedocs.py')
app.run()
```

The configuration file will configure both the frontend webapp and
the backend search engine.

Several example configuration files are given in the `config/`
directory of this repository. Additionally, several configuration
files used in tests are in the `tests/` directory.

## General Info

The centillion configuration file is a Python file that mainly
contains variable declarations. These configuration variables
are passed into the centillion Flask app, and are also passed
through to the search backend.

The configuration file has the following sections:

* Access Control
* Testing
* Searching
* User Interface
* Github
* Google Drive
* Disqus
* Flask


## Example config files

The main example configuration file is located at

```
config/config_centillion.example.py
```

There are three other example configuration files
in that directory. These are configuration files
for running a centillion instance with a search
index populated by fake documents, Google Drive
documents, and Github files/issues/pull requests
(respectively):

```
config/config_centillion_fakedocs.py
config/config_centillion_gdrive.py
config/config_centillion_gh.py
```

The `tests/` directory contains three additional
configuration files that are similar to the three
example config files above.

