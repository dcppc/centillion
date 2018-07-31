# Components

The components of centillion are as follows:
- Flask application, which creates a Search object and uses it to search index
- Search object, which allows you to create/update/search an index

## Routes layout

Current application routes are as follows:

- home -> search
- search
- update_index

Ideal application routes (using github flask dance oauth):

- home
    - if not logged in, landing page
    - if logged in, redirect to search
- search
- main_index_update
    - update main index, all docs period
- delta_index_update
    - updates delta index, docs that have changed since last main index

There should be one route to update the main index

There should be another route to update the delta index

These should go off and call the update index methods
for each respective type of document/collection.
For example, if I call `main_index_update` route it should

- call `main_index_update` for all github issues
- call `main_index_update` for folder of markdown docs
- call `main_index_update` for google drive folder

These are all members of the Search class

## Functions layout

Functions of the entire search app:
- create a search index
- load a search index
- call the search() method on the index
- update the search index

The first and last, creating and updating the search index,
are of greatest interest.

The Schema affects everything so it is hard to separate
functionality into a main Search class shared by many.
(Avoid inheritance/classes if possible.)

current Search:
- open_index creates the schema
- add_issue or add_document adds an item to the index
- add_all_issues or add_all_documents iterates over items and adds them to index
- update_index_incremental - update the search index
- create_search_results - package things up for jinja
- search - run the query, pass results to the jinja-packager


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


Nice to have but focus on it later:

- update_diff_issues or update_diff_md or update_diff_documents iterates over items
  and indexes recently-added items

- update_diff_index - update the diff search index (what's been added since last
  time)
    - calls all three update_diff methods






## Files layout

Schema definition:
* include a "kind" or "class" to group objects
* can provide different searches of different collections
* eventually can provide user with checkboxes





