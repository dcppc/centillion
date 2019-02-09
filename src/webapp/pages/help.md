# Help Page: centillion

This page provides some guidance on using centillion,
the document search engine.

## What does centillion index?

centillion indexes the following:

- Google Drive files
  folder (the entire contents of docx files are indexed,
  while only the metadata is indexed for non-docx files)

- Github issues and pull requests (both open and closed)

- Github files (the entire contents of Markdown files
  are indexed, only the metadata is indexed for
  non-Markdown files)

- Disqus comment threads



### Basic Searching: Single-Term Searches

To run a basic search, just type a search term into the text box and click "Search."

Try the following search terms:

<div class="alert alert-info" role="alert">
pineapple
</div>

<div class="alert alert-info" role="alert">
orange
</div>

<div class="alert alert-info" role="alert">
banana
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
"no way"
</div>

<div class="alert alert-info" role="alert">
"he left without the"
</div>

<div class="alert alert-info" role="alert">
"laser sharks"
</div>

Note that if you search for a term (for example
`"laser sharks"`) with _double quotes_, centillion
will ignore anything in the search index where the word
`"laser"` and the word `"sharks"` are not contiguous.

The exception is stop words. For example, searching for
`"laser sharks"` will also find the phrase 
`"sharks anad lasers"`.


### Search Operators

The `AND` and `OR` operators are available for users in
centillion. However, _these operators must be CAPITALIZED_
or they will be interpreted as literal words!

To include any item in the search index that contains
the word `"sharks"` and contains the word `"lasers"`, 
but where the two words are not necessarily next to each other,
use the `AND` operator:

<div class="alert alert-info" role="alert">
sharks AND lasers
</div>

This can also be used with multi-word phrases, using
double quotes accordingly: to search for all documents
containing the word `sharks` and the phrase
`"laser helmet"`, pass both to centillion with `AND`:

<div class="alert alert-info" role="alert">
sharks AND "laser helmet"
</div>

You can also use the OR operator to return any
documents containing one or the other or both of the
given search term or phrase. For example, to seach for
any documents involving garlic or onions,

<div class="alert alert-info" role="alert">
garlic OR onions
</div>

Finally, these operators can be combined by wrapping
statements in parentheses. For example, suppose we
wanted to look for all information about either
garlic or onions, and only if related to cooking
or to vampires.

We can combine the two `AND` searches with an `OR`:

<div class="alert alert-info" role="alert">
(garlic OR onions) AND (cooking OR vampires)
</div>


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
  files in Github repositories), and "disqus" (Disqus comment threads)

* `title` - title of the document

* `owner_name` - the name of the owner of the Google Drive file
  (permissions/ownership information comes from Google via their API)
  (this field is not set for Github items)

* `owner_email` - the email address of the Google Drive file owner (this
  information is not set for Github items)

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
</div>

<div class="alert alert-info" role="alert">
created_time:2018 aug 4th
</div>

<div class="alert alert-info" role="alert">
created_time:august 5 2018
</div>

<div class="alert alert-info" role="alert">
created_time:28 july 2018
</div>

Dates without a year can also be specified,
as can entire months:

<div class="alert alert-info" role="alert">
modified_time:august 5
</div>

<div class="alert alert-info" role="alert">
modified_time:july 2018
</div>

To construct a date range, use the word "to"
to connect two dates:

<div class="alert alert-info" role="alert">
modified_time:august 28 to september 2
</div>

<div class="alert alert-info" role="alert">
modified_time:july 2018 to august 2018
</div>


### Searching Specific Fields

To search only a specific field for a search term, include the field name, a
colon, and the search term you wish to search for. Use double quotes for
phrases, as usual.

For example, the following will find all Google Drive files or Groups.io email
threads created by Santa Claus:

<div class="alert alert-info" role="alert">
owner_name:"Santa Claus"
</div>

To expand this search to include things on Github, 
too, we can include Santa's Github handle using the
`github_user` field search:

<div class="alert alert-info" role="alert">
owner_name:"Santa Claus" OR github_user:"realsanta"
</div>

