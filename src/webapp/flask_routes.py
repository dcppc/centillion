from .const import base, call
from .flask_index_task import UpdateIndexTask

from ..search import Search

from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, request, redirect, url_for, abort, render_template
from flask import Markup, flash, jsonify
from flask_dance.contrib.github import make_github_blueprint, github

import os
import sys
import json
import logging
import markdown
import codecs
import subprocess

from datetime import datetime


"""
Centillion Flask Routes:

Call the method that decorates the Flask app
with all routes.
"""


def setup_routes(app):

    if app.config['AUTHENTICATION_LAYER']:
        client_id = app.config['GITHUB_OAUTH_CLIENT_ID']
        client_secret = app.config['GITHUB_OAUTH_CLIENT_SECRET']

        # Make the github login blueprint
        github_bp = make_github_blueprint(
                                client_id = client_id,
                                client_secret = client_secret,
                                scope='read:org')

        app.register_blueprint(github_bp, url_prefix="/login")

    last_searches_file = app.config["INDEX_DIR"] + "/last_searches.txt" 



    ##############################
    # Github authentication layer
    # implemented as decorator

    class centillion_github_auth(object):
        """
        Decorator class to provide a
        Github authentication layer
        on top of Flask routes
        """
        def __init__(self,enabled=True,admin=False,is_landing_page=False):
            # is auth layer enabled?
            self.enabled = enabled
            # is this the landing page?
            self.is_landing_page = is_landing_page
            # is this an admin-only page?
            self.admin = admin

        def __call__(self,*args,**kwargs):
            """Return a function that takes a function
            """
            # If the auth layer is disabled, this decorator
            # just passes the function on through
            if self.enabled is False:
                def f(g):
                    return g(*args,**kwargs)
                return f


            # If the auth layer is enabled, this decorator
            # will use the Github API and the user/org
            # whitelists in the config file to control
            # access to the web frontend of the 
            # centillion instance.
            def new_function(old_function):
                if not github.authorized:
                    if self.is_landing_page:
                        return render_template("landing.html")
                    else:
                        return redirect(url_for("github.login"))

                try:
                    username_payload = github.get('/user').json()
                    username = username_payload['login']
                except KeyError:
                    err = "ERROR: Could not find 'login' key from /user endpoint of Github API, "
                    err += "may have hit rate limit.\n"
                    err += "Payload:\n"
                    err += "%s"%(username_payload)
                    logging.exception(err)
                    return render_template('404.html')

                # The admin setting in the config file
                # affects which whitelist we use to 
                # control access to the page. 
                # 
                # If this is an admin page,
                # use the admin whitelist, &c.
                if self.admin:
                    logins_whitelist = app.config['ADMIN_WHITELIST_GITHUB_LOGINS']
                    orgs_whitelist   = app.config['ADMIN_WHITELIST_GITHUB_ORGS']
                    teams_whitelist  = app.config['ADMIN_WHITELIST_GITHUB_TEAMS']
                else:
                    logins_whitelist = app.config['WHITELIST_GITHUB_LOGINS']
                    orgs_whitelist   = app.config['WHITELIST_GITHUB_ORGS']
                    teams_whitelist  = app.config['WHITELIST_GITHUB_TEAMS']

                if username in logins_whitelist:
                    old_function(*args, **kwargs) # Proceed

                # For each of the user's organizations,
                # see if any are on the orgs whitelist
                resp = github.get("/user/orgs")
                if resp.ok:
                    all_orgs = resp.json()
                    for org in all_orgs:
                        if org['login'] in orgs_whitelist:
                            old_function(*args, **kwargs) # Proceed

                # For each of the team IDs on the whitelist,
                # check if the user is a member of that team
                for teamid in teams_whitelist:
                    teamresp = github.get('/teams/%s/members/%s'%(copper_team_id,username))
                    if mresp.status_code==204:
                        old_function(*args, **kwargs) # Proceed

                # User is not on any whitelists
                return render_template('403.html')
    
            return new_function



    ##############################
    # Flask routes

    #@centillion_github_auth(is_landing_page=True)
    @centillion_github_auth
    @app.route('/')
    def index():
        # Business as usual
        return redirect(url_for("search", query="", fields=""))
    
    @centillion_github_auth
    @app.route('/log_in')
    def log_in():
        # Business as usual
        return redirect(url_for("search", query="", fields=""))

    @centillion_github_auth
    @app.route('/search')
    def search():
        # Business as usual
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
            store_search(query,fields)
    
        totals = search.get_document_total_count()
    
        return render_template('search.html', 
                               entries=result, 
                               query=query, 
                               parsed_query=parsed_query, 
                               fields=fields, 
                               totals=totals)


    @centillion_github_auth
    @app.route('/master_list')
    def master_list():
        """Serve the master list page, which has a
        master list of all types of documents 
        contained in the search index.
        """
        return render_template("masterlist.html") # Proceed


    @centillion_github_auth
    @app.route('/list/<doctype>')
    def list_docs(doctype):
        """Given a document type, return a JSON list
        of all documents matching that type in the
        search index.
        Example: /list/gdocs
        """
        search = Search(app.config["INDEX_DIR"])
        results_list = search.get_list(doctype)
        for result in results_list:
            if 'created_time' in result.keys():
                ct = result['created_time']
                result['created_time'] = datetime.strftime(ct,"%Y-%m-%d %I:%M %p")
            if 'modified_time' in result.keys():
                mt = result['modified_time']
                result['modified_time'] = datetime.strftime(mt,"%Y-%m-%d %I:%M %p")
            if 'indexed_time' in result.keys():
                it = result['indexed_time']
                result['indexed_time'] = datetime.strftime(it,"%Y-%m-%d %I:%M %p")
        return jsonify(results_list)




    @centillion_github_auth
    @app.route('/feedback', methods=['POST'])
    def parse_request():
        try:
            data = request.form.to_dict();
            data['github_login'] = username
            data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
            feedback_database = 'feedback_database.json'
            if not os.path.isfile(feedback_database):
                with open(feedback_database,'w') as f:
                    json_data = [data]
                    json.dump(json_data, f, indent=4)
    
            else:
                json_data = []
                with open(feedback_database,'r') as f:
                    json_data = json.load(f)
    
                json_data.append(data)
    
                with open(feedback_database,'w') as f:
                    json.dump(json_data, f, indent=4)
    
            ## Should be done with Javascript
            #flash("Thank you for your feedback!")
            return jsonify({'status':'ok','message':'Thank you for your feedback!'})
        except:
            return jsonify({'status':'error','message':'An error was encountered while submitting your feedback. Try submitting an issue in the <a href="https://github.com/dcppc/centillion/issues/new">dcppc/centillion</a> repository.'})


    @centillion_github_auth
    @app.route('/help')
    def help():
        """Serve up the Help page by rendering it
        from Markdown to HTML.
        """
        help_md = os.path.join(base,'pages','help.md')
        with open(help_md,'r') as f:
            content = Markup(markdown.markdown(f.read()))
        return render_template("help.html",**locals())


    @centillion_github_auth
    @app.route('/faq')
    def faq():
        """Serve up the FAQ page by rendering it
        from Markdown to HTML.
        """
        faq_md = os.path.join(base,'pages','faq.md')
        with open(faq_md,'r') as f:
            content = Markup(markdown.markdown(f.read()))
        return render_template("faq.html",**locals())


    ######################
    # Admin flask routes

    @centillion_github_auth(admin=True)
    @app.route('/update_index/<run_which>')
    def update_index(run_which):
        """Update the centillion search index.
        """
        # This is the task that links into the
        # search submodule of centillion.
        UpdateIndexTask(
                app.config,
                run_which = run_which
        )
        flash("Rebuilding index, check console output")
        # This redirects user to /control_panel route
        # to prevent accidental re-indexing
        return redirect(url_for("control_panel"))


    @centillion_github_auth(admin=True)
    @app.route('/control_panel')
    def control_panel():
        """Access the control panel interface to
        re-index the database.
        """
        return render_template("controlpanel.html") # Proceed


    ###############
    # Other routes

    @app.errorhandler(404)
    def oops(e):
        return render_template('404.html')
    
    
    def store_search(query, fields):
        """
        Store searches in a text file
        """
        if os.path.exists(last_searches_file):
            with codecs.open(last_searches_file, 'r', encoding='utf-8') as f:
                contents = f.readlines()
        else:
            contents = []
    
        search = "query=%s&fields=%s\n" % (query, fields)
        if not search in contents:
            contents.insert(0, search)
    
        ### # Record history of searches
        ### if not os.path.exists(last_searches_file):
        ###     subprocess.call(['touch',last_searches_file])
        ### with codecs.open(last_searches_file, 'w', encoding='utf-8') as f:
        ###     f.writelines(contents)

