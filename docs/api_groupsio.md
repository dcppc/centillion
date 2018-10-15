## How does centillion use the Groups.io API?

We use the Groups.io endpoint to get the archive of each
subgroup in mbox format, in a zip file. We extract it and
parse each email, and add them all to the search index.

Calling the Groups.io API requires that you create an API
access token. See the `scripts/` directory for a script that
will create a new Groups.io API access token.

