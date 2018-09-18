# centillion: Help Page

This page provides some guidance on using centillion,
the Data Commons search engine.

## What does centillion index?

centillion indexes the following:

- Google Drive files in the Data Commons Google Drive
  folder (the entire contents of docx files are indexed,
  while only the metadata is indexed for non-docx files)

- Github issues and pull requests (both open and closed)
  in all of the [DCPPC Github organization's](https://github.com/dcppc)
  Github repositories (both public and private)

- Github files (the entire contents of Markdown files
  are indexed, only the metadata is indexed for
  non-Markdown files)

- Groups.io email threads for the [DCPPC group](https://dcppc.groups.io/)
  on Groups.io

- Disqus comment threads on the internal DCPPC site,
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

If you use a multi-word phrase, centillion will split
the phrase into individual words, and look for
occurrences of each word in the search index. If you
would rather centillion search for an exact phrase,
enter it in double quotes.

Try the following search terms - then try them without
the double quotes to see what chages:

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

Note that if you search for a term (for example
`"onboarding process"`) with _double quotes_, centillion
will ignore anything in the search index where the word
`"onboarding"` and the word `"process"` are not contiguous.

The exception is stop words. For example, searching for
`"onboarding process"` will also find the phrase 
`"process of onboarding"`.


### Search Operators

The `AND` and `OR` operators are available for users in
centillion. However, _these operators must be CAPITALIZED_
or they will be interpreted as literal words!

To include any item in the search index that contains
the word `"onboarding"`` and the word `"whitelist"`, but 
not necessarily next to each other, use the `AND` operator:

<div class="alert alert-info" role="alert">
onboarding AND whitelist
</div>

This can also be used with multi-word phrases, using
double quotes accordingly: to search for all documents
containing the word `onboarding` and the phrase
`"full stack"`, pass both to centillion with `AND`:

<div class="alert alert-info" role="alert">
onboarding AND "full stack"
</div>

You can also use the OR operator to return any
documents containing one or the other or both of the
given search term or phrase. For example, to seach for
any documents involving Team Oxygen or Team Calcium,

<div class="alert alert-info" role="alert">
oygen OR calcium
</div>

Finally, these operators can be combined by wrapping
statements in parentheses. For example, suppose we
wanted to look for all information about either
onboarding or whitelisting, and only if related to Team
Copper or Team Phosphorus. We can combine the two `AND`
searches with an `OR`:

<div class="alert alert-info" role="alert">
(onboarding OR whitelisting) AND (copper OR phosphorus OR phosphorous)
</div>

Side note: phosphorus is a special case, as its correct
spelling ("phosphorus") is not as common as the incorrect
spelling ("phosphorous").


### Advanced Search: Searching By Field Name

Each document indexed by centillion has several
fields and associated values. A full list of fields
is given below.

By default, searches will be run against several
common fields. To run a search against a particular
field only, specify the name of the field, then a
colon (no spaces), then the search term:

<div class="alert alert-info" role="alert">
field_name:foo
</div>

Use quotes to surround multi-word search terms:

<div class="alert alert-info" role="alert">
field_name:'foo bar baz'
</div>

This runs a search against the field `field_name`
of all documents in the search index and returns
documents containing foo, bar, and baz.

Note that if we accidentally forgot quotes, 
`field_name:foo bar baz` would be equivalent to

<div class="alert alert-info" role="alert">
field_name:foo AND bar AND baz
</div>

(This is _definitely not_ what the user meant!)

There cannot be _any_ space before or after the colon,
or the field name will be interpreted as a search term 
instead. 

### Advanced Search: All Field Names

You can also conduct searches on specific fields in the search index. The
search index schema contains the following fields:

* `kind` - can be one of "gdoc" (Google Drive file), "issue" (Github issue),
  "markdown" (Markdown files in Github repositories), "ghfile" (non-Markdown
  files in Github repositories), "emailthread" (Groups.io email thread), and
  "disqus" (Disqus comment threads)
* `title` - title of the document
* `owner_name` - the name of the owner of the Google Drive file
  (permissions/ownership information comes from Google via their API), or the
  original sender of the Groups.io email thread (this field is not linked to
  Github items)
* `owner_email` - the email address of the Google Drive file owner (this
  information is not linked to Github items or Groups.io items)
* `github_user` - for Github files and issues, the Github @user is the only
  info available
* `content` - the field containing the entire contents of each document

Documents also have three fields containing date and time information:

* `created_time` - date and time stamp for when this item was created
* `modified_time` - date and time stamp for when this item was modified


### Advanced Search: Dates and Times

The date and time fields can be searched using a variety
of ways of specifying a date or a date range.
Date searches are different from other searches:
the name of the datetime field is considered part
of the search.

First, a single day can be specified, and any date and time
stamps that fall between the start and end of that day
will be returned.

<div class="alert alert-info" role="alert">
created_time:20180912
created_time:2018 aug 4th
created_time:august 5 2018
created_time:28 july 2018
</div>

Dates without a year can also be specified,
as can entire months:

<div class="alert alert-info" role="alert">
modified_time:august 5
modified_time:july 2018
</div>

To construct a date range, use the word "to"
to connect two dates:

<div class="alert alert-info" role="alert">
modified_time:august 28 to september 2
modified_time:july 2018 to august 2018
</div>


### Searching Specific Fields

To search only a specific field for a search term, include the field name, a
colon, and the search term you wish to search for. Use double quotes for
phrases, as usual.

For example, the following will find all Google Drive files or Groups.io email
threads created by Titus Brown:

<div class="alert alert-info" role="alert">
owner_name:"Titus Brown"
</div>

To expand this search to include things on Github, too, we can include a
`github_user` field search as well: 

<div class="alert alert-info" role="alert">
owner_name:"Titus Brown" OR github_user:"ctb"
</div>

