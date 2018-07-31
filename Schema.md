# Schema

Define a single mixed schema.

## The Centillion Schema

The Centillion Schema:

```
id = ID(stored=True, unique=True),

created_time = ID(stored=True),
modified_time = ID(stored=True),
indexed_time = ID(stored=True),

title = TEXT(stored=True),
url = ID(stored=True, unique=True),

mimetype=ID(stored=True),
owner_email=ID(stored=True),
owner_name=TEXT(stored=True),

repo_name=TEXT(stored=True),
repo_url=ID(stored=True),

issue_title=TEXT(stored=True, field_boost=100.0),
issue_url=ID(stored=True),

github_user=TEXT(stored=True),

content=TEXT(stored=True, analyzer=stemming_analyzer)
```

## Centillion Schema Examples

The Centillion Cheeseburger (Google Drive): 
the centillion schema applied to google drive files.

```
id                  | ok
created_time        | ok
modified_time       | ok
indexed_time        | ok
title               | ok
url                 | ok
drive_mimetype      | ok
drive_owner_email   | ok
drive_owner_name    | ok
repo_name           | -
repo_url            | -
issue_title         | -
issue_url           | -
gh_user             | -
content             | ?
```

The Centillion Embarcadero (Github Issues):
the centillion schema applied to github issues and comments.

```
id                  | ok
created_time        | ok
modified_time       | ?
indexed_time        | ok
title               | ok
url                 | ok
drive_mimetype      | -
drive_owner_email   | -
drive_owner_name    | -
repo_name           | ok
repo_url            | ok
issue_title         | ok
issue_url           | ok
gh_user             | ok
content             | ok
```

The Centillion Markdown Inside Github Repos:
the centillion schema applied to markdown files inside github repos.

```
id                  | ok
created_time        | ok
modified_time       | ok
indexed_time        | ok
title               | ok
url                 | ok
drive_mimetype      | -
drive_owner_email   | -
drive_owner_name    | -
repo_name           | ok
repo_url            | ok
issue_title         | ok
issue_url           | ok
gh_user             | ?
content             | ok
```

The Centillion Just Plain Old Markdown:
the centillion schema applied to markdown files in a folder on disk.


```
id                  | ok
created_time        | ok
modified_time       | ok
indexed_time        | ok
title               | ok
url                 | -
drive_mimetype      | -
drive_owner_email   | -
drive_owner_name    | -
repo_name           | -
repo_url            | -
issue_title         | -
issue_url           | -
gh_user             | -
content             | ok
```








Cheeseburger:

```
id=ID(stored=True,unique=True),
url=ID(stored=True, unique=True),
mimetype=ID(stored=True),
timestamp=ID(stored=True),
owner_email=ID(stored=True),
owner_name=ID(stored=True),
title=TEXT(stored=True),
content=TEXT(stored=True, analyzer=stemming_analyzer)
```

Issues:

```
url=ID(stored=True, unique=True),
is_comment=BOOLEAN(stored=True),
timestamp=STORED,
repo_name=TEXT(stored=True),
repo_url=ID(stored=True),
issue_title=TEXT(stored=True, field_boost=100.0),
issue_url=ID(stored=True),
user=TEXT(stored=True),
content=TEXT(stored=True, analyzer=stemming_analyzer)
```

Markdown in a github repo:

```
url = 
title = 
url =
repo_name = 
repo_url = 
content = 
```

Markdown:

```
path=path,
filename=file_name,
headlines=parser.headlines,
content=content,
time = modtime
```



