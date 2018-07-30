# Schema

Define a single mixed schema.

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

Markdown:

```
path=path,
filename=file_name,
headlines=parser.headlines,
content=content,
time = modtime
```



