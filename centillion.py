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
"""



