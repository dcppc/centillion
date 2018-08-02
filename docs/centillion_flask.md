# Centillion Flask

## What the flask server does

Flask is a web server framework
that allows developers to define
behavior for specific endpoints,
such as `/hello_world`, or
<http://localhost:5000/hello_world>
on a web server running locally.

## Flask server routes

- `/home`
    - if not logged in, this redirects to a "log into github" landing page (not implemented yet)
    - if logged in, this redirects to the search route

- `/search`
    - search template

- `/main_index_update`
    - update main index, all docs period

- `/control_panel`
    - this is the control panel, where you can trigger
      the search index to be re-made




