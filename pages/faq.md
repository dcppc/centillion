# FAQ Page: centillion

This page answers some common questions about
centillion, the Data Commons search engine.

<br />
 
### What does centillion index?

centillion indexes the following:

* Google Drive files in the Data Commons Google Drive
  folder (the entire contents of docx files are indexed,
  while only the metadata is indexed for non-docx files)
* Github issues and pull requests (both open and closed)
  in all of the DCPPC Github organization's Github
  repositories
* Github files (the entire contents of Markdown files
  are indexed, only the metadata is indexed for
  non-Markdown files)
* Groups.io email threads
* Disqus comment threads on the internal DCPPC site,
  <https://pilot.nihdatacommons.us>

<br />
 
### What doesn't centillion index?

centillion utilizes a special DCPPC bot account to
access Google Drive files and Github content.

centillion **does not** utilize the Github or Google Drive
credentials of any Data Commons users.

centillion **does not** index any content in your personal
Github account or your personal Google Drive.

We respect your privacy!

<br />

### How often does centillion re-index?

The content indexed by centillion is updated on a regular basis
but how often depends on the type of content.

* Google Drive files are re-indexed daily
* Github issues are re-indexed daily
* Github files and repo contents are re-indexed daily
* Groups.io email threads are indexed infrequently
  due to API limitations.

<br />
 
### Why does centillion need my Github login?

Due to the fact that centillion indexes internal and
potentailly non-public documents, access to centillion
is limited to members of the Data Commons. To verify a
centillion user is a member of the Data Commons, we
require users to log in via Github.com and have Github
check if a user is a member of the @dcppc organization.

**At no point** does centillion ever handle your Github
password.

<br />
 
### How does licensing work? Does centillion claim ownership of any content?

No - centillion does not claim ownership of any content it indexes.

* Because the search engine is protected behind a Github authentication layer, there is no risk of internal, non-public documents being made public (or licensed information being released into the wild).
* Because bot accounts are used to access Google Drive documents and Github resources, there is no way for centillion to modify the ownership of content.
* centillion is a search index, and not a content management system. Documents are not transferred to centillion or stored as a part of the search index process. Search results from centillion will link to all original content and make ownership information clear whenever possible.

<br />

### What information does centillion collect about me?

centillion anonymizes and logs all queries that are run.
These queries are not associated with IP address information.
Tracking queries that are being run helps us improve the
quality of centillion and identify trending topics.
centillion and identify trending topics.

centillion will log your IP address as part of the
analytics information it collects, but no IP addresses
will be tied to search terms. 

