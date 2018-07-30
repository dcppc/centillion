# Components

The components of centillion are as follows:
- Flask application, which creates a Search object and uses it to search index
- Search object, which allows you to create/update/search an index

The application routes are as follows:
- home -> search
- update_index
- search


## The Ideal App

the ideal app:
- Flask application, uses a Search object to search index
- Search object to create/update/search index
- We have to live with SOME duplication

Application routes with oauth github flask dance authentication:
- home
    - if not logged in, landing page
    - if logged in, redirect to search
- delta_index_update
    - updates delta index, docs that have changed since last main index
- main_index_update
    - update main index, all docs period
- search


