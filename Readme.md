# centillion

![version number](https://img.shields.io/badge/version-1.8.0-blue.svg)
[![travis](https://img.shields.io/travis/charlesreid1/centillion.svg)](https://travis-ci.org/charlesreid1/centillion)

**centillion**: a document search engine that searches
across Github issues, Github pull requests, Github files,
Google Drive documents, and Disqus comment threads.

**a centillion**: a very large number consisting of a 1 with 303 zeros after it.

One centillion is 3.03 log-times better than a googol.

![Screenshot: centillion search](images/search.png)


## What is centillion

centillion is a search engine that can index different kinds of document
collections: Google Documents (.docx files), Google Drive files, Github issues,
Github files, Github Markdown files, and Disqus comment threads.


## How centillion works

The backend of centillion defines how documents are obtained and how
the search index is constructed. centillion builds and updates the
search index by using APIs to get the latest versions of documents,
and updates its search index accordingly.

The centillion frontend provides a web interface for running queries
and interfacing with the search index. ([More information](frontend.md))


## How to configure centillion

To get started with centillion, you will need to create
a centillion configuration file. Start with the example
configuration file in the `examples/` directory.


## Quickstart

This quickstart will get you started with a centillion
instance that is populated with fake documents (avoiding
the need to make real API calls). This will allow you
to try out centillion before you enable any APIs.

**Clone:**

Start by cloning a copy of the repo:

```
cd
git clone https://github.com/dcppc/centillion
cd ~/centillion/
```

**Virtual Environment:**

(This step is optional.)

Start by setting up a virtual environment, where centillion
will be installed:

```
virtualenv vp
source vp/bin/activate
```

**Install:** 

To install centillion, first install the required packages:

```
pip install -r requirements.txt
```

Now install centillion:

```
python setup.py build install
```

Test that your centillion installation went okay:

```
python -m centillion
```

If you see no output, that means centillion has been successfully installed.
If you see an error message, check that you have activated your virtual
environment (`source vp/bin/activate`).

**Run:** 

Crete a temporary working directory:

```
mkdir -p /tmp/my-centillion-instance && cd /tmp/my-centillion-instance
```

Now create a minimal centillion instance with the following
Python program:

**`run_centillion.py`:**

```
import centillion

app = centillion.webapp.get_flask_app(config_file='config.py')
app.run()
```

The `config.py` file can be copied verbatim from the example
configuration file in the repository:

```
cp ~/centillion/config/config_centillion.example.py config.py
```

Now run the centillion instance by running the script:

```
python run_centillion.py
```

This will run the webapp on port 5000, so navigate to
<http://localhost:5000> in the browser.

**Populate the Search Index:**

To populate the search index, visit the control panel route:

<http://localhost:5000/control_panel>

From here you can re-index the search engine. The example
configuration file uses fake documents instead of real API
calls, so the reindexing will work even without a network
connection. To return to the index, click the centillion 
banner.

**Visit the Master List:**

The master list shows a list of every document indexed by
centillion. Visit the master list route:

<http://localhost:5000/master_list>

**Try Searching:**

Visit the help page for more information about running searches:

<http://localhost:5000/help>

Try searching for the following terms to see search results:

* `barley`
* `masked figure`
* `bananas`
* `bacteria`
* `microscope`




## Resources for centillion

centillion on Github: <https://github.com/dcppc/centillion>

centillion documentation: <http://dcppc.github.io/centillion>

