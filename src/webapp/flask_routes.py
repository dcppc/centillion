from .const import base, call

from flask import Flask, request, abort, render_template
import os, sys
import json
import logging


"""
Flask Routes:

Call the method that decorates the Flask app
with all routes.
"""


def setup_routes(app):


    #################
    # TODO: FIX THIS

    @app.route('/', methods=['GET', 'POST'])
    def index():
    
        # forgot to add the dang render template handler
        if request.method=='GET':
            return render_template("index.html")
    
        config = app.config
    
        # Verify webhooks are from github
        verify_github_source(config)
    
        # Play ping/pong with github
        event = request.headers.get('X-GitHub-Event')
        if event == 'ping':
            return json.dumps({'msg': 'pong'})
    
        # Get the payload
        payload = get_payload(request)
    
        # Enforce secret
        enforce_secret(config,request)
    
        # Get the branch
        branch = get_branch(payload)
    
        # Current events almost always have a repository.
        # Be safe in case they do not.
        name = payload['repository']['name'] if 'repository' in payload else None
    
        # Assemble quick lookup info
        meta = {
            'name': name,
            'branch': branch,
            'event': event
        }
    
        app.init_payload_handler()
        payload_handler = app.get_payload_handler()
        payload_handler.process_payload(payload, meta, config)
        app.del_payload_handler()
    
        # Clean up
        return json.dumps({'status':'done'})



