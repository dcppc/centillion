# FAQ Page: centillion

This page answers some common questions about
centillion, the document search engine.

<br />
 
### What does centillion index?

centillion can index any of the following:

* Google Drive files accessible to a given Google account
  (the entire contents of docx files are indexed,
  while only the metadata is indexed for non-docx files)
* Github issues and pull requests (both open and closed)
  in any repository that a given Github account has 
  access to
* Github files (the entire contents of Markdown files
  are indexed, only the metadata is indexed for
  non-Markdown files)
* Disqus comment threads 

<br />
 
### What doesn't centillion index?

To index content, it must be accessible to the accounts
whose API keys are provided in the config file.

<br />

### How often does centillion re-index?

The re-indexing operation must be performed manually.
Visit the `/control_panel` endpoint to update the
index by individual document type, or to update
all document types at once.

<br />
 
### Why does centillion need my Github login?

If the centillion Github authentication layer is 
turned on, only Github users who are members of a
whitelisted organization or whose account names
are whitelisted may access centillion.

To do this, we use a Github OAuth application to
verify your identity via Github. This requires you
to log in to Github using your Github account.

**At no point** does centillion ever handle your Github
password.
 
