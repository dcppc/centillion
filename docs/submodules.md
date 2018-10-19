## Submodules of centillion

centillion is implemented as a Python package that can be installed using
`setup.py` and imported using `import centillion`.

The package is structured as two submodules - a backend `search` submodule,
and a frontend `webapp` submodule.

### Backend: `search` submodule

See [Backend](backend.md) for details.

The search submodule implements objects and functions to create or update
the search index on disk, load an existing search index, and performing
searches with user-provided queries.

### Frontend: `webapp` submodule

See [Frontend](frontend.md) for details.

The webapp submodule implements the Flask frontend, sets up the 
Flask routes, implements the Github authentication layer, and 
serves up static content and Jinja templates.

