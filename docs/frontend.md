## Frontend: User access control

Because centillion indexes internal and private documents for the Data Commons
project, centillion implements a Github authentication layer on top of the Flask
server. This authentication layer asks users to log in with their Github accounts,
and if the user is a member of the DCPPC organization, they are granted access to the
centillion website.

We use [flask-dance](https://github.com/singingwolfboy/flask-dance) to implement
the Github authentication layer.

![Screen shot: centillion authentication](images/auth.png)


## Frontend: Flask routes


### Route: `/master_list`

There is a master list of all content indexed by centilion at the master list page,
<https://search.nihdatacommons.us/master_list>.

A master list for each type of document indexed by the search engine is displayed
in a table:

![Screen shot: centillion master list](docs/images/master_list.png)

The metadata shown in these tables can be filtered and sorted:

![Screen shot: centillion master list with sorting](docs/images/master_list2.png)


### Route: `/control_panel`

The centillion control panel is located at <https://search.nihdatacommons.us/control_panel>.
The control panel allows you to rebuild the search index from scratch.  The
search index stores versions/contents of files locally, so re-indexing involves
going out and asking each API for new versions of a file/document/web page.
When you re-index the main search index, it will ask every API for new versions
of every document.  You can also update only specific types of documents in the
search index.

![Screen shot: centillion control panel](docs/images/control_panel.png)



