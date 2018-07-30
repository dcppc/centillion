# Schema

Currently in a tug-of-war between improving individual components,
which creates more work in the porting-over step, or just integrating
everything (half baked as it is) into  single tool and improving 
from there.

Which makes me wonder if there is a third way?

- modular components that live side-by-side
- issues search plugin
- google drive search plugin
- problem: each module has to (painstakingly) define a schema

We are going to have to rewrite the schema at some point,
but don't worry for now about handling templates/bundlers/everything else.

The bigger concern is getting the search engine working.

Define a single mixed schema.

