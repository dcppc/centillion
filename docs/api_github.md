## How does centillion use the Github API?

centillion indexes several types of documents from
Github. First, all issues and pull requests are
indexed, including the full text of the comment 
thread. Second, the names and paths to files in 
Github repositories are indexed. The content of
the file is only indexed if the file is a Markdown
file.

## What kind of Github API keys are used?

to be able to index issues, pull requests, and 
files, centillion uses the Github API to access
these resources and index their content automatically.
This requires the use of an **API access token**.

To access issues, pull requests, and files in private
repositories, the API access token must be created 
by an account with access to the appropriate resources.

## How is the API key provided?

An API access token can be created in the Github
account settings page. The access token is provided
in the centillion configuration file.

See [backend#Configuration](backend.md#Configuration)
for info about the configuration file.

## How is the Github authentication layer set up?

The Github authentication layer uses an OAuth application
(which must be created and set up with a callback URL
ahead of time) to ask users to log in, and check if they
are part of the appropriate organization.

To use the application to request organization membership
information from users logging in through centillion,
API keys must be provided for the OAuth application to
verify ownership of the application.

See [Github authentication layer](auth.md) page for details.

