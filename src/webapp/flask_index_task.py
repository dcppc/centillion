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

Define a class to handle updating the search index.

This class spawns a new thread to collect 
information from the respective API and use 
it to update the search index in the background.

IMPORTANT: This class is the glue between the 
webapp and search submodules.
"""


class UpdateIndexTask(object):
    def __init__(self, app_config, run_which='all'):
        self.run_which = run_which
        self.app_config = app_config
        if self.app_config['FAKEDOCS']:
            print("Found FAKEDOCS = True in config file, running test update index task")
            thread = threading.Thread(target=self.test, args=())
        else:
            print("Found FAKEDOCS = False in config file, running real update index task")
            thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()


    def test(self):
        """
        Run the test update index method to populate the
        search index with fake documents.
        """
        # Load the search index
        search = Search(self.app_config["INDEX_DIR"])

        # Update the index with fake docs
        search.test_update_index(self.run_which,
                                 self.app_config)


    def run(self):
        """Run the actual update index task against live APIs.
        """
        # Load API credentials
        self.gh_token       = self.app_config['GITHUB_TOKEN']
        self.disqus_token   = self.app_config['DISQUS_TOKEN']

         #Load the search index
        search = Search(self.app_config["INDEX_DIR"])

        # Update the index with real docs
        search.update_index(self.gh_token,
                            self.disqus_token,
                            self.run_which,
                            self.app_config)

