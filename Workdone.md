## work that is done

**Stage 1: index folder of markdown files** (done)
* See [markdown-search](https://git.charlesreid1.com/charlesreid1/markdown-search.git)
* Successfully using whoosh to index a directory of Markdown files
    * Problem: .git directory cannot be present (or contaminates list of
      indexed directories)
    * Problem: search index stored on disk, not clear how to use on Heroku
    * May need to check in binary search index, or dive headfirst into
      sqlalchemy
    * Not using [pypandoc](https://github.com/bebraw/pypandoc) yet to extract 
      header/emphasis information

Needs work:

* <s>More appropriate schema</s>
* Using more features (weights) plus pandoc filters for schema
* Sqlalchemy (and hey waddya know safari books has it covered)


**Stage 2: index a repo's github issues** (done)
* See [issues-search](https://git.charlesreid1.com/charlesreid1/issues-search.git)
* Successfully using whoosh to index a repository's issues and comments
* Use PyGithub
* Main win here is uncovering metadata/linking/presentation issues

Needs work:
- <s>treat comments and issues as separate objects, fill out separate schema fields
- map out and organize how the schema is updated to make it more flexible
- configuration needs to enable user to specify organization+repos</s>

```plain
{
    "to_index" : [
        "google/google-api-python-client",
        "microsoft/TypeCode",
        "microsoft/api-guielines"
    }
}
```


**Stage 3: index documents in a google drive folder** (done)
* See [cheeseburger-search](https://git.charlesreid1.com/charlesreid1/cheeseburger-search.git) 
* Successfully using whoosh to index a Google Drive
    * File names/owners
    * For documents, pandoc to extract content
    * Searchable by document content
* Use the google drive api (see simple-simon)
* Main win is more uncovering of metadata issues, identifying
  big-picture issues for centillion
