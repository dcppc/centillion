## How does centillion use the Github API?

centillion indexes several types of documents from
Github. First, all issues and pull requests are
indexed, including the full text of the comment 
thread. Second, the names and paths to files in 
Github repositories are indexed. The content of
the file is only indexed if the file is a Markdown
file.

centillion needs to index private documents in 
private Github repositories, so it needs to use
an API key associated with an account with the
necessary permissions. To access issues, pull
requests, and repository contents, centillion
requires **an API access token**. This is provided
in the centillion configuration file.

There is also a Github authentication layer 
that prevents unauthorized access to the search
engine and its contents (because of private
documents, as mentioned above). This requires
**a Github OAuth application API token and secret.** 
The OAuth application needs to verify a Github
user is a member of a particular Github 
organization. The OAuth token and secret are
provided via the centillion configuration file.


