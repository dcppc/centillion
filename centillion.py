import threading
from subprocess import call

import codecs
import os
from flask import Flask, request, redirect, url_for, render_template, flash

# create our application
from centillion_search import Search


"""
The Centillion

The centillion is a search engine that indexes the following:
    - Folder of Markdown documents
    - Github issues
    - Google Drive folder

You provide:
    - Github API key via env var
    - Google Drive API key via file
"""

class UpdateIndexTask(object):
    def __init__(self, diff_index=False):
        self.diff_index = diff_index
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        search = Search(app.config["INDEX_DIR"])

        if(self.diff_index):
            raise Exception("diff index not implemented")

        credentials_file = 'credentials.json'
        collection = 'charlesreid1dib test collection'
        search.update_index_incremental(credentials_file,
                                        app.config)

app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.from_pyfile("config.py")

last_searches_file = app.config["INDEX_DIR"] + "/last_searches.txt"


##############################
# Flask routes


@app.route('/')
def index():
    return redirect(url_for("search", query="", fields=""))

@app.route('/search')
def search():
    query = request.args['query']
    fields = request.args.get('fields')
    if fields == 'None':
        fields = None

    search = Search(app.config["INDEX_DIR"])
    if not query:
        parsed_query = ""
        result = []

    else:
        parsed_query, result = search.search(query.split(), fields=[fields])
        store_search(query, fields)

    total = search.get_document_total_count()

    return render_template('search.html', entries=result, query=query, parsed_query=parsed_query, fields=fields, last_searches=get_last_searches(), total=total)

@app.route('/open')
def open_file():
    path = request.args['path']
    fields = request.args.get('fields')
    query = request.args['query']
    call([app.config["EDIT_COMMAND"], path])

    return redirect(url_for("search", query=query, fields=fields))

@app.route('/update_index')
def update_index():
    rebuild = request.args.get('rebuild')
    UpdateIndexTask(diff_index=False)
    flash("Rebuilding index, check console output")
    return render_template("search.html", query="", fields="", last_searches=get_last_searches())


##############
# Utility methods

def get_last_searches():
    if os.path.exists(last_searches_file):
        with codecs.open(last_searches_file, 'r', encoding='utf-8') as f:
            contents = f.readlines()
    else:
        contents = []
    return contents

def store_search(query, fields):
    if os.path.exists(last_searches_file):
        with codecs.open(last_searches_file, 'r', encoding='utf-8') as f:
            contents = f.readlines()
    else:
        contents = []

    search = "query=%s&fields=%s\n" % (query, fields)
    if not search in contents:
        contents.insert(0, search)

    with codecs.open(last_searches_file, 'w', encoding='utf-8') as f:
        f.writelines(contents[:30])

if __name__ == '__main__':
    app.run()

