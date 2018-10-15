## Backend: Technologies

centillion is a Python program built using
[whoosh](https://bitbucket.org/mchaput/whoosh) (search
engine library).  It indexes the full text of docx files
in Google Documents, just the filenames for non-docx
files. The full text of issues and their comments are
indexed, and results are grouped by issue. centillion
requires Google Drive and Github OAuth apps. The
credentials to access these services via their respective
APIs can be accomplished by providing the API credentials
via the centillion configuration file.

## Backend: Configuration

To configure centillion, you should provide a single configuration file that 
specifies configuration details for both the webapp frontend and the serach 
backend. There is an example configuration file in the repo at:

```
conf/config_flask.example.py
```

The location of this configuration file should be passed in to the program
running centillion via the `CENTILLION_CONFIG` environment variable. For 
example, if the program `examples/run_centillion.py` contains a script that
imports centillion and runs the webapp, you can pass the config file using the
`CENTILLION_CONFIG` environment variable like this:

```
CENTILLION_CONFIG="conf/config_flask.py" python examples/run_centillion.py
```

## Backend: Schema

Following is a list of fields contained in the 
search index schema. (These are not all defined
for all document.)

* `id`
* `kind`
* `fingerprint`
* `created_time`
* `modified_time`
* `indexed_time`
* `title`
* `url`
* `mimetype`
* `owner_email`
* `owner_name`
* `repo_name`
* `repo_url`
* `issue_title`
* `issue_url`
* `github_user`
* `content`


