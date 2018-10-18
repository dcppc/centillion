# Backend

## Technologies

centillion is a Python program built using
[whoosh](https://bitbucket.org/mchaput/whoosh) (search
engine library).  It indexes the full text of docx files
in Google Documents, just the filenames for non-docx
files. The full text of issues and their comments are
indexed, and results are grouped by issue. centillion
requires Google Drive and Github OAuth apps. The
credentials to access these services via their respective
APIs can be accomplished by providing the API credentials
via the centillion configuration file.

Also see [APIs](api_all.md) page.


## Configuration

See [Configuring centillion](config.md) page.


## Search class

The `centillion_search.py` file defines a
`Search` class that serves as the backend
for centillion.

### What the Search class does

The `Search` class has two roles:

- create (and update) the search index
  (this also requires the `Search` class
  to define the schema for storing documents)

- run queries against the search index and 
  prepare the query results to be rendered 
  by Flask using Jinja templates

### Methods implemented by the search class

The Search class implements the following methods:

- `update_index` (update entire search index)
- `open_index` (create new schema, open index on disk)

- `add_drive_file` (add an individual google drive file item)
- `add_issue` (add an individual github issue item)
- `add_ghfile` (add an individual github file item)
- `add_emailthread` (add groups.io email thread item)
- `add_disqusthread` (add disqus comments thread)

- `update_index_gdocs` (iterate over all Google Drive documents and add them)
- `update_index_issues` (iterate over all Github issues and add them)
- `update_index_ghfiles` (iterate over all github files and add them)
- `update_index_emailthreads` (iterate over all groups.io subgroup email threads and add them)
- `update_index_disqus` (iterate over all disqus comment threads and add them)

- `create_search_results` (package search results for the Flask template)
- `get_document_total_count` (ask centillion for count of documents of each type)
- `get_list` (get a listing of all files of a particular type)

- `search` (perform a search on the search index with the user's query)


## Search Index Schema

### Schema fields

Following is a list of fields contained in the 
search index schema. (These are not all defined
for all document.)

* `id`
* `kind`
* `fingerprint`
* `created_time`
* `modified_time`
* `indexed_time`
* `title`
* `url`
* `mimetype`
* `owner_email`
* `owner_name`
* `repo_name`
* `repo_url`
* `issue_title`
* `issue_url`
* `github_user`
* `content`

### Translating new items into the schema

centillion contains support for Google Drive,
Github, Groups.io, and Disqus APIs. 

If you want to add a new API with new types of items,
you need to map the fields of the new type of items 
that centillion will index to the search index schema
fields above.

Not every item needs to define every field. However, 
if the schema needs new fields added to it, the entire
search index will need to be re-built (may be 
time-consuming).

