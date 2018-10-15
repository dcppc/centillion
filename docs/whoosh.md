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




# New

Define a Search object for use by the centillion search engine.

Auth notes:
    - Google drive/Google oauth requires credentials.json
    - Github oauth requires api token passed in via Flask config

Utility functions:
    - clean_timestamp (for cleanup of timestamps)
    - is_url (for cleanup of results)
    - SearchResult (simple class representing results)
    - DontEscapeHtmlInCodeRenderer (used to render markdown as html)

Search class:
    - update_index (update entire search index)
    - open_index (create new schema, open index on disk)

    - add_drive_file (add an individual google drive file item)
    - add_issue (add an individual github issue item)
    - add_ghfile (add an individual github file item)
    - add_emailthread (add groups.io email thread item)
    - add_disqusthread (add disqus comments thread)

    - update_index_gdocs (iterate over all Google Drive documents and add them)
    - update_index_issues (iterate over all Github issues and add them)
    - update_index_ghfiles (iterate over all github files and add them)
    - update_index_emailthreads (iterate over all groups.io subgroup email threads and add them)
    - update_index_disqus (iterate over all disqus comment threads and add them)

    - create_search_results (package search results for the Flask template)
    - get_document_total_count (ask centillion for count of documents of each type)
    - get_list (get a listing of all files of a particular type)

    - search (perform a search on the search index with the user's query)

Schema:
    - id
    - kind
    - fingerprint
    - created_time
    - modified_time
    - indexed_time
    - title
    - url
    - mimetype
    - owner_email
    - owner_name
    - repo_name
    - repo_url
    - issue_title
    - issue_url
    - github_user
    - content
