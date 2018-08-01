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


## quickstart

Run the centillion app with a github access token API key set via
environment variable:

```
GITHUB_TOKEN="XXXXXXXX" python centillion.py
```

This will start a Flask server, and you can view the minimal search engine
interface in your browser at <http://localhost:5000>.

## more info

For more info see the documentation: <https://charlesreid1.github.io/centillion>




