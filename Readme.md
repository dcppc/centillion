# The Centillion

**centillion**: a pan-github-markdown-issues-google-docs search engine.

**a centillion**: a very large number consisting of a 1 with 303 zeros after it.

one centillion is 3.03 log-times better than a googol.

![Screen shot of centillion](docs/images/ss.png)


## what is it

Centillion (https://github.com/dcppc/centillion) is a search engine that can index 
three kinds of collections: Google Documents, Github issues, and Markdown files in 
Github repos.

We define the types of documents the centillion should index,
what info and how. The centillion then builds and
updates a search index. That's all done in `centillion_search.py`.

The centillion also provides a simple web frontend for running
queries against the search index. That's done using a Flask server
defined in `centillion.py`.

The centillion keeps it simple.

## authentication layer

Centillion lives behind a Github authentication layer, implemented with 
[flask-dance](https://github.com/singingwolfboy/flask-dance). When you first
visit the site it will ask you to authenticate with Github so that it can 
verify you have permission to access the site.

## technologies

Centillion is a Python program built using whoosh (search engine library). It
indexes the full text of docx files in Google Documents, just the filenames for
non-docx files. The full text of issues and their comments are indexed, and
results are grouped by issue. Centillion requires Google Drive and Github OAuth
apps. Once you provide credentials to Flask you're all set to go. 


## control panel

There's also a control panel at <https://search.nihdatacommons.us/control_panel> 
that allows you to rebuild the search index from scratch (the Google Drive indexing 
takes a while).

![Screen shot of centillion control panel](docs/images/cp.png)


## quickstart (with Github auth)

Start by creating a Github OAuth application.
Get the public and private application key 
(client token and client secret token)
from the Github application's page.
You will also need a Github access token
(in addition to the app tokens).

When you create the application, set the callback
URL to `/login/github/authorized`, as in:

```
https://<url>/login/github/authorized
```

Edit the Flask configuration `config_flask.py`
and set the public and private application keys.

Now run centillion:

```
python centillion.py
```

or if you used http instead of https:

```
OAUTHLIB_INSECURE_TRANSPORT="true" python centillion.py
```

This will start a Flask server, and you can view the minimal search engine
interface in your browser at `http://<ip>:5000`.


## troubleshooting

If you are having problems with your callback URL being treated
as HTTP by Github, even though there is an HTTPS address, and
everything else seems fine, try deleting the Github OAuth app
and creating a new one.

