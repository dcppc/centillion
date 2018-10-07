from .const import base, call

from flask import Flask, request, abort, render_template
import os, sys
import json
import logging


"""
Centillion Flask App

This class defines a Flask app that will
load a custom config file, as specified
by the FLASK_CONFIG environment variable.



TODO:
    FIX CONFIG ENV VAR
    FLASK VERSUS CENTILLION
    HOW TO LOAD PYTHON FILE

# Load default config and override config from an environment variable
app.config.from_pyfile("config_flask.py")
"""


class CentillionFlask(Flask):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        # ----------------------------
        # Load config file
        msg = "CentillionFlask: __init__(): Preparing to load webapp config file."
        logging.info(msg)
        loaded_config = False

        # Option 1:
        # The user can set the centillion config file
        # using the CENTILLION_CONFIG variable when
        # they run their driver
        cf = 'CENTILLION_CONFIG'
        if cf in os.environ:

            # If the config file is in the 
            # current working directory:
            if os.path.isfile(os.path.join(call,os.environ[cf])):
                # relative path
                self.config.from_pyfile(os.path.join(call,os.environ[cf]))
                loaded_config = True
                msg = "CentillionFlask: __init__(): Succesfuly loaded webapp config file from CENTILLION_CONFIG variable.\n"
                msg += "Loaded config file at %s"%(os.path.join(call,os.environ[cf]))
                logging.info(msg)
        
            # If the config file is 
            # an absolute path:
            elif os.path.isfile(os.environ[cf]):
                # absolute path
                self.config.from_pyfile(os.environ['UNCLE_ARCHIE_CONFIG'])
                loaded_config = True
                msg = "CentillionFlask: __init__(): Succesfuly loaded webapp config file from UNCLE_ARCHIE_CONFIG variable.\n"
                msg += "Loaded config file at %s"%(os.environ['UNCLE_ARCHIE_CONFIG'])
                logging.info(msg)
        
        else:
            err = "CentillionFlask: __init__(): Warning: No UNCLE_ARCHIE_CONFIG environment variable defined. "
            err += "Looking for 'config.py' in current directory."
            logging.info(err)

            # hail mary: look for config.py in the current directory
            default_name = 'config.py'
            if os.path.isfile(os.path.join(call,default_name)):
                self.config.from_pyfile(os.path.join(call,default_name))
                loaded_config = True
                msg = "CentillionFlask: __init__(): Succesfuly loaded webapp config file with a hail mary.\n"
                msg += "Loaded config file at %s"%(os.path.join(call,'config.py'))
                logging.info(msg)

        if not loaded_config:
            err = "ERROR: CentillionFlask: __init__(): Problem setting config file with %s environment variable\n"%(cf)
            try:
                err += "%s value : %s\n"%(cf,os.environ[cf])
            except:
                pass

            try:
                err += "Missing config file : %s\n"%(os.environ[cf])
                err += "Missing config file : %s\n"%(os.path.join(call, os.environ[cf]))
            except:
                pass

            logging.exception(err)
            raise Exception(err)

