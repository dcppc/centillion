# Centillion Help

This page provides some guidance on using centillion, the Data Commons search engine.

### What Does Centillion Index?

Centillion indexes the following:

* Google Drive files in the Data Commons Google Drive folder (the entire contents
  of docx files are indexed, while only the metadata is indexed for non-docx files)
* Github issues and pull requests (both open and closed) in all of the 
  [DCPPC Github organization's](https://github.com/dcppc)
  Github repositories
* Github files (the entire contents of Markdown files are indexed, only the metadata
  is indexed for non-Markdown files)
* Groups.io email threads
* Disqus comment threads on the internal DCPPC site,
  <https://pilot.nihdatacommons.us>


### Basic Searching: Single-Term Searches

To run a basic search, just type a search term into the text box and click "Search."

Try the following search terms:

<div class="alert alert-info" role="alert">
onboarding
</div>

<div class="alert alert-info" role="alert">
oxygen
</div>

<div class="alert alert-info" role="alert">
fullstack
</div>

### Basic Searching: Multi-Term Searches

If you use a multi-word phrase, centillion will split the phrase into individual words,
and look for occurrences of each word in the search index. If you would rather centillion
search for an exact phrase, **enter it in double quotes.**

Try the following search terms - then try them without the double quotes to see what chages:

<div class="alert alert-info" role="alert">
"analysis pipeline"
</div>

<div class="alert alert-info" role="alert">
"onboarding process"
</div>

<div class="alert alert-info" role="alert">
"full stacks"
</div>

<div class="alert alert-info" role="alert">
"deliverables due"
</div>

Note that if you search for a term (for example `"onboarding process"`)
with double quotes, centillion will ignore anything in the search 
index that contains the word "onboarding" separate from the word 
"process".

The exception is stop words. For example, searching for `"onboarding process"`
will also find the phrase `"process of onboarding"`.


### AND/OR Operators

The AND and OR operators are available for users in centillion.
However, these operators must be CAPITALIZED or they will be
interpreted as literal words!

To include any item in the search index that contains the word "onboarding"
and the word "whitelist", but not necessarily next to each other, use the AND
operator:

<div class="alert alert-info" role="alert">
onboarding AND whitelist
</div>

This can also be used with multi-word phrases, using double quotes accordingly:
to search for all documents containing the word "onboarding" and the phrase
"full stack", pass these both to AND (quotes and all):

<div class="alert alert-info" role="alert">
onboarding AND "full stack"
</div>

You can also use the OR operator to return any documents containing one or the other or both
of the given search term or phrase. For example, to seach for any documents involving
Team Oxygen or Team Calcium,

<div class="alert alert-info" role="alert">
oygen OR calcium
</div>

Finally, these operators can be combined by wrapping statements in parentheses.
For example, suppose we wanted to look for all information about either 
onboarding or whitelisting, and only if related to Team Copper or Team Phosphorus.
We can combine the two AND searches with an OR:

<div class="alert alert-info" role="alert">
(onboarding OR whitelisting) AND (copper OR phosphorus OR phosphorous)
</div>

Side note: phosphorus is a special case, as its correct spelling ("phosphorus")
is not as common as the incorrect spelling "phosphorous". 

### Advanced Search: List of Fields

You can also conduct searches on specific fields in the search index.
The search index schema contains the following fields:

* `kind` - can be one of "gdoc" (Google Drive file), "issue" (Github issue),
  "markdown" (Markdown files in Github repositories), "ghfile" (non-Markdown files
  in Github repositories), "emailthread" (Groups.io email thread), and "disqus"
  (Disqus comment threads)
* `title` - title of the document
* `owner_name` - the name of the owner of the Google Drive file (permissions/ownership
  information comes from Google via their API), or the original sender of the 
  Groups.io email thread (this field is _not_ linked to Github items)
* `owner_email` - the email address of the Google Drive file owner (this information is
  _not_ linked to Github items or Groups.io items)
* `github_user` - for Github files and issues, the Github @user is the only info available
* `content` - the field containing the entire contents of each document

Fields of limited usefulness for advanced searches:

* `url` - the URL of the document (must be an exact match)
* `created_time` - advanced searches with date/time fields is not currently implemented.
* `indexed_time` - see above
* `modified_time` - see above


### Searching Specific Fields

To search only a specific field for a search term, include the field name, a colon, and the search
term you wish to search for. Use double quotes for phrases, as usual.

For example, the following will find all Google Drive files or Groups.io email threads created by
Titus Brown:

<div class="alert alert-info" role="alert">
owner_name:"Titus Brown"
</div>

To expand this search to include things on Github, too, we can include a `github_user` field search
as well:

<div class="alert alert-info" role="alert">
owner_name:"Titus Brown" OR github_user:"ctb"
</div>


