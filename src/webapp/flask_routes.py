from .const import base, call

from ..search import Search

from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, request, abort, render_template
from flask import Markup
from flask_dance.contrib.github import make_github_blueprint, github

import os
import sys
import json
import logging


"""
Centillion Flask Routes:

Call the method that decorates the Flask app
with all routes.
"""


def setup_routes(app):

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
    # Flask routes

    @app.route('/')
    def index():
        if not github.authorized:
            return render_template("landing.html")
        else:
            username = github.get("/user").json()['login']
            resp = github.get("/user/orgs")
            if resp.ok:
    
                # If they are in dcppc, redirect to search.
                # Otherwise, hit em with a 403
                all_orgs = resp.json()
                for org in all_orgs:
                    if org['login']=='dcppc':
                        # Business as usual
                        return redirect(url_for("search", query="", fields=""))
    
                # Not in dcppc
                return render_template('403.html')
    
            # Could not reach Github
            return render_template('404.html')
    
    
    @app.route('/log_in')
    def log_in():
        if not github.authorized:
            return redirect(url_for("github.login"))
        else:
            username = github.get("/user").json()['login']
            resp = github.get("/user/orgs")
            if resp.ok:
    
                # If they are in dcppc, redirect to search.
                # Otherwise, hit em with a 403
                all_orgs = resp.json()
                for org in all_orgs:
                    if org['login']=='dcppc':
                        # Business as usual
                        return redirect(url_for("search", query="", fields=""))
    
                # Not in dcppc
                return render_template('403.html')
    
            # Could not reach Github
            return render_template('404.html')
    
    
    
    @app.route('/search')
    def search():
        if not github.authorized:
            return redirect(url_for("github.login"))
        username = github.get("/user").json()['login']
        resp = github.get("/user/orgs")
        if resp.ok:
    
            # If they are in dcppc, show them search.html
            # Otherwise, hit em with a 403
            all_orgs = resp.json()
            for org in all_orgs:
                if org['login']=='dcppc':
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
    
            # Not in dcppc 
            return render_template('403.html')
    
        # Could not reach Github
        return render_template('404.html')
    
    
    @app.route('/update_index/<run_which>')
    def update_index(run_which):
        """
        TEAM COPPER ONLY!!!
        """
        if not github.authorized:
            return redirect(url_for("github.login"))
        username = github.get("/user").json()['login']
        resp = github.get("/user/orgs")
        if resp.ok:
    
            # Only Team Copper members can update the index
            all_orgs = resp.json()
            for org in all_orgs:
                if org['login']=='dcppc':
                    copper_team_id = '2700235'
                    mresp = github.get('/teams/%s/members/%s'%(copper_team_id,username))
                    if mresp.status_code==204:
                        # Business as usual
                        UpdateIndexTask(app.config,
                                        diff_index=False,
                                        run_which = run_which)
                        flash("Rebuilding index, check console output")
                        # This redirects user to /control_panel route
                        # to prevent accidental re-indexing
                        return redirect(url_for("control_panel"))
    
        return render_template('403.html')
    
    
    @app.route('/control_panel')
    def control_panel():
        """
        TEAM COPPER ONLY!!!
        """
        if not github.authorized:
            return redirect(url_for("github.login"))
        username = github.get("/user").json()['login']
        resp = github.get("/user/orgs")
        if resp.ok:
    
            # Only Team Copper members can access the control panel
            all_orgs = resp.json()
            for org in all_orgs:
                if org['login']=='dcppc':
                    copper_team_id = '2700235'
                    mresp = github.get('/teams/%s/members/%s'%(copper_team_id,username))
                    if mresp.status_code==204:
                        # Business as usual
                        return render_template("controlpanel.html")
    
            # Not in dcppc 
            return render_template('403.html')
    
        # Could not reach Github
        return render_template('404.html')
    
    
    
    @app.route('/master_list')
    def master_list():
        if not github.authorized:
            return redirect(url_for("github.login"))
        username = github.get("/user").json()['login']
        resp = github.get("/user/orgs")
        if resp.ok:
    
            # If they are in dcppc, show them masterlist.html
            # Otherwise, hit em with a 403
            all_orgs = resp.json()
            for org in all_orgs:
                if org['login']=='dcppc':
                    # Business as usual
                    return render_template("masterlist.html")
    
            # Not in dcppc 
            return render_template('403.html')
    
        # Could not reach Github
        return render_template('404.html')
    
    
    
    @app.route('/list/<doctype>')
    def list_docs(doctype):
        if not github.authorized:
            return redirect(url_for("github.login"))
        username = github.get("/user").json()['login']
        resp = github.get("/user/orgs")
        if resp.ok:
            all_orgs = resp.json()
            for org in all_orgs:
                if org['login']=='dcppc':
                    # Business as usual
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
    
        # nope
        return render_template('403.html')



    @app.route('/feedback', methods=['POST'])
    def parse_request():
    
        if not github.authorized:
            return redirect(url_for("github.login"))
        username = github.get("/user").json()['login']
        resp = github.get("/user/orgs")
        if resp.ok:
            all_orgs = resp.json()
            for org in all_orgs:
                if org['login']=='dcppc':
    
    
                    try:
                        # Business as usual
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
    
    
        # nope
        return render_template('403.html')
    
    
    
    @app.route('/help')
    def help():
        if not github.authorized:
            return redirect(url_for("github.login"))
        username = github.get("/user").json()['login']
        resp = github.get("/user/orgs")
        if resp.ok:
    
            # If they are in dcppc, show them help
            # Otherwise, hit em with a 403
            all_orgs = resp.json()
            for org in all_orgs:
                if org['login']=='dcppc':
                    # Business as usual
                    help_md = os.path.join(base,'pages','help.md')
                    with open(help_md,'r') as f:
                        content = Markup(markdown.markdown(f.read()))
                    return render_template("help.html",**locals())
    
            # Not in dcppc 
            return render_template('403.html')
    
        # Could not reach Github
        return render_template('404.html')
    
    

    @app.route('/faq')
    def faq():
        if not github.authorized:
            return redirect(url_for("github.login"))
        username = github.get("/user").json()['login']
        resp = github.get("/user/orgs")
        if resp.ok:
    
            # If they are in dcppc, show them faq
            # Otherwise, hit em with a 403
            all_orgs = resp.json()
            for org in all_orgs:
                if org['login']=='dcppc':
                    # Business as usual
                    faq_md = os.path.join(base,'pages','faq.md')
                    with open(faq_md,'r') as f:
                        content = Markup(markdown.markdown(f.read()))
                    return render_template("faq.html",**locals())
    
            # Not in dcppc 
            return render_template('403.html')
    
        # Could not reach Github
        return render_template('404.html')



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
    
        # TODO: Fix this to record information more cleanly
        with codecs.open(last_searches_file, 'w', encoding='utf-8') as f:
            f.writelines(contents)


