# The Centillion

**the centillion**: a pan-github-markdown-issues-google-docs search engine.

**a centillion**: a very large number consisting of a 1 with 303 zeros after it.

the centillion is 3.03 log-times better than the googol.

![Screen shot of centillion](img/ss.png)

## what is it

The centillion is a search engine built using [whoosh](https://whoosh.readthedocs.io/en/latest/intro.html),
a Python library for building search engines.

We define the types of documents the centillion should index,
what info and how. The centillion then builds and
updates a search index. That's all done in `centillion_search.py`.

The centillion also provides a simple web frontend for running
queries against the search index. That's done using a Flask server
defined in `centillion.py`.

The centillion keeps it simple.


## quickstart (with Github auth)

Start by creating a Github OAuth application.
Get the public and private application key from the Github
settings page.

Set the callback URL to `/login/github/authorized`, as in:

```
https://<url>:5000/login/github/authorized
```

(You can also use http if you must.)

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

## more info

For more info see the documentation: <https://charlesreid1.github.io/centillion>




