# Centillion Whoosh

The `centillion_search.py` file defines a
`Search` class that serves as the backend
for centillion.

## What the Search class does

The `Search` class has two roles:
- create (and update) the search index
    - this also requires the `Search` class
      to define the schema for storing documents
- run queries against the search index,
  and package results up for Flask and Jinja

## Search class functions

The `Search` class defines several functions:

- `open_index()` creates the schema

- `add_issue()`, `add_md()`, `add_document()` have three diff method sigs and add diff types
  of documents to the search index

- `update_all_issues()` or `update_all_md()` or `update_all_documents()` iterates over items
  and determines whether each item needs to be updated in the search index

- `update_main_index()` - update the entire search index
    - calls all three update_all methods

- `create_search_results()` - package things up for jinja

- `search()` - run the query, pass results to the jinja-packager

