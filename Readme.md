# centillion

**the centillion**: a pan-github-markdown-issues-google-docs search engine.

**a centillion**: a very large number consisting of a 1 with 303 zeros after it.

the centillion is 3.03 log-times better than the googol.

## what is it

The centillion is a search engine built using [whoosh](#),
a Python library for building search engines.

We define the types of documents the centillion should index,
and how, using what fields. The centillion then builds and
updates a search index. That's all done in `centillion_search.py`.

The centillion also provides a simple web frontend for running
queries against the search index. That's done using a Flask server
defined in `centillion.py`.

The centillion keeps it simple.


## work that is done

See [Workdone.md](Workdone.md)


## work that is being done

See [Workinprogress.md](Workinprogress.md) for details about
route and function layout. Summary below.

### code organization

centillion app routes:

- home
    - if not logged in, landing page
    - if logged in, redirect to search
- search
- main_index_update
    - update main index, all docs period


centillion Search functions:

- open_index creates the schema

- add_issue, add_md, add_document have three diff method sigs and add diff types
  of documents to the search index

- update_all_issues or update_all_md or update_all_documents iterates over items
  and determines whether each item needs to be updated in the search index

- update_main_index - update the entire search index
    - calls all three update_all methods

- create_search_results - package things up for jinja

- search - run the query, pass results to the jinja-packager


## work that is planned

See [Workplanned.md](Workplanned.md)

