# Testing Architecture

Due to the complicated nature of centillion tests, we need to use Docker
containers to run the different types of tests involved.

## Test Pod: Description

**Backend Test Container:** 

The principal centillion docker container will be flask + whoosh.
This will be run via docker compose and will expose port 5000 to
the local pod network.

This container will run any internal tests of core centillion functionality.
This will populate the search index with content in the process, so that it
is ready for UI testing.

**Frontend Test Container:**

A second UI test docker container will run tests that interact
with the centillion UI, but do not import centillion directly or use
its code.

## Task List

To do testing right, we really need to change centillion to use a package
structure. We can structure it as a webapp submodule and a search submodule.

This triggers other to do items:

- dealing with config files
- logging 
- validation
- where to put the search index

Other longer term items:

- generalizing centillion
- making it OOP
- search schema specifications


