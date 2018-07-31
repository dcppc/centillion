# Components

The components of centillion are as follows:
- Flask application, which creates a Search object and uses it to search index
- Search object, which allows you to create/update/search an index

## Routes layout

Centillion flask app routes:

- `/home`
    - if not logged in, landing page
    - if logged in, redirect to search
- `/search`
- `/main_index_update`
    - update main index, all docs period

## Functions layout

Centillion Search class functions:

- `open_index()` creates the schema

- `add_issue()`, `add_md()`, `add_document()` have three diff method sigs and add diff types
  of documents to the search index

- `update_all_issues()` or `update_all_md()` or `update_all_documents()` iterates over items
  and determines whether each item needs to be updated in the search index

- `update_main_index()` - update the entire search index
    - calls all three update_all methods

- `create_search_results()` - package things up for jinja

- `search()` - run the query, pass results to the jinja-packager

Nice to have but focus on it later:
- update diff search index (what's been added since last index time)
    - max index time


## Files layout

Schema definition:
* include a "kind" or "class" to group objects
* can provide different searches of different collections
* eventually can provide user with checkboxes

