from ..search import Search

import threading
import subprocess
import markdown

import codecs
import os, json
from datetime import datetime

from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, request, redirect, url_for, render_template, flash, jsonify
from flask import Markup
from flask_dance.contrib.github import make_github_blueprint, github


"""
Centillion Flask: Index Task

This class represents the task that updates
the search index. This essentially provides
the glue between the webapp submodule and 
the search submodule. 
"""


class UpdateIndexTask(object):
    def __init__(self, app_config, run_which='all'):
        self.run_which = run_which
        self.app_config = app_config
        thread = threading.Thread(target=self.run, args=())

        self.gh_token = app_config['GITHUB_TOKEN']
        self.groupsio_token = app_config['GROUPSIO_TOKEN']
        self.disqus_token = app_config['DISQUS_TOKEN']
        thread.daemon = True
        thread.start()

    def run(self):
        search = Search(self.app_config["INDEX_DIR"])

        search.update_index(self.groupsio_token,
                            self.gh_token,
                            self.disqus_token,
                            self.run_which,
                            self.app_config)


