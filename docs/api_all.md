## APIs used

The centillion configuration file must contain API keys for each of the following
third-party services:

* Github (see [How does centillion use the Github API](api_github.md))
* Groups.io (see [How does centillion use the Groups.io API](api_groupsio.md))
* Google Drive (see [How does centillion use the Google Drive API](api_gdrive.md))
* Disqus (see [How does centillion use the Disqus API](api_disqus.md))

### Github

Github API credentials (both an OAuth token for the centillion app's Github
authentication mechanism, and a personal access token for accessing repositories
during the re-indexing process) are provided in `config_flask.py`.

### Groups.io

The Groups.io API token is used to index email threads. This token is provided in
`config_flask.py`.

### Google Drive

The Google Drive API credentials are provided in a file, `credentials.json`. This is
the file that is generated when the OAuth process is complete.

When you enable the Google Drive API in the Google Cloud Console, you will be provided
with a file `client_secrets.json`. To authenticate centillion with Google Drive, you should
download this file, and run the Google Drive utility directly:

```
python scripts/prepare_gdrive.py
```

This will initiate the authentication procedure. Sign in as a user that has access to
the documents you want to index, and _only_ the documents you want to index (it is useful
to set up a bot account for this purpose).

Once you log in as that user, it will create `credentials.json`, and the Google Drive
re-indexing procedure should not have any problems authenticating using that file.

`credentials.json` must be present in the same directory as the program being run.

