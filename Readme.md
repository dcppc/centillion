# centillion

**the centillion**: a pan-github-markdown-issues-google-docs search engine.

**a centillion**: a very large number consisting of a 1 with 303 zeros after it.

the centillion is 3.03 log-times better than the googol.

## what is it

The centillion is a search engine built using [whoosh](#),
a Python library for building search engines.

We define the types of documents the centillion should index,
and how, using what fields. The centillion then builds and
updates a search index.

The centillion also provides a simple web frontend for running
queries against the search index.

The centillion keeps it simple.


## work that is done

**Stage 1: index folder of markdown files** (done)
* See [markdown-search](https://git.charlesreid1.com/charlesreid1/markdown-search.git)
* Successfully using whoosh to index a directory of Markdown files
    * Problem: .git directory cannot be present (or contaminates list of
      indexed directories)
    * Problem: search index stored on disk, not clear how to use on Heroku
    * May need to check in binary search index, or dive headfirst into
      sqlalchemy
    * Not using [pypandoc](https://github.com/bebraw/pypandoc) yet to extract 
      header/emphasis information

Needs work:

* More appropriate schema
* Using more features (weights) plus pandoc filters for schema
* Sqlalchemy (and hey waddya know safari books has it covered)


**Stage 2: index a repo's github issues** (done)
* See [issues-search](https://git.charlesreid1.com/charlesreid1/issues-search.git)
* Successfully using whoosh to index a repository's issues and comments
* Use PyGithub
* Main win here is uncovering metadata/linking/presentation issues

Needs work:
- treat comments and issues as separate objects, fill out separate schema fields
- map out and organize how the schema is updated to make it more flexible
- configuration needs to enable user to specify organization+repos

```plain
{
    "to_index" : {
        "google" : "google-api-python-client",
        "microsoft" : ["TypeCode","api-guidelines"]
    }
}
```


**Stage 3: index documents in a google drive folder** (done)
* See [cheeseburger-search](https://git.charlesreid1.com/charlesreid1/cheeseburger-search.git) 
* Successfully using whoosh to index a Google Drive
    * File names/owners
    * For documents, pandoc to extract content
    * Searchable by document content
* Use the google drive api (see simple-simon)
* Main win is more uncovering of metadata issues, identifying
  big-picture issues for centillion


## immediate next steps

### code organization

See [Components.md](Components.md) for the battle plan.

centillion app:

- home
    - if not logged in, landing page
    - if logged in, redirect to search
- search
- main_index_update
    - update main index, all docs period


centillion Search:

- open_index creates the schema

- add_issue, add_md, add_document have three diff method sigs and add diff types
  of documents to the search index

- update_all_issues or update_all_md or update_all_documents iterates over items
  and determines whether each item needs to be updated in the search index

- update_main_index - update the entire search index
    - calls all three update_all methods

- create_search_results - package things up for jinja

- search - run the query, pass results to the jinja-packager


## future work

### whoosh

Whoosh:
- fix templates
    - indexed folders thing
    - cut it out!
    - clean up template styles some
- test/figure out integrated schema
    - can we use None for irrelevant field values?
    - jinja template updates?
    - can use boolean values, change display based on that

### rewriting

Licensing:
- need to start from scratch
- unpack markdown functionality
- replace it

Flask routes:
-protecting with github-flask-dance
- <s>organizing delta/main index updates</s>

### heroku

Stateless
- Use SqlAlchemy to make stateless
- Convert to Heroku-enabled script



