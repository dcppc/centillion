from .const import base, call

from flask import Flask, request, abort, render_template
import os, sys
import json
import logging


"""
Centillion Flask App

Extend the Flask class for centillion.

This Flask class gets a config file name
from an environment varible, and attempts
to load it and set it as the Flask config.

NOTE: to load a Python file as a Flask 
config file, use:
>>> app.config.from_pyfile("config_flask.py")
"""


class CentillionFlask(Flask):
    """
    Extend the Flask class to load a config file
    on initialization.

    The CENTILLION_CONFIG environment variable
    specifies the file location. This is then
    loaded as a Flask config file.
    """
    def __init__(self,*args,**kwargs):
        """
        Do everything the parent does.
        Then load the config file.
        """
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
                msg = "CentillionFlask: __init__(): Succesfuly loaded webapp config file from %s variable.\n"%(cf)
                msg += "Loaded config file at %s"%(os.path.join(call,os.environ[cf]))
                logging.info(msg)
        
            # If the config file is 
            # an absolute path:
            elif os.path.isfile(os.environ[cf]):
                # absolute path
                self.config.from_pyfile(os.environ[cf])
                loaded_config = True
                msg = "CentillionFlask: __init__(): Succesfuly loaded webapp config file from %s variable.\n"%(cf)
                msg += "Loaded config file at %s"%(os.environ[cf])
                logging.info(msg)
        
        else:
            err = "CentillionFlask: __init__(): Warning: No %s environment variable defined. "%(cf)
            err += "Looking for 'config.py' in current directory."
            logging.info(err)

            # hail mary: look for config.py in the current directory
            default_name = 'config.py'
            if os.path.isfile(os.path.join(call,default_name)):
                self.config.from_pyfile(os.path.join(call,default_name))
                loaded_config = True
                msg = "CentillionFlask: __init__(): Succesfuly loaded webapp config file with a hail mary.\n"
                msg += "Loaded config file at %s"%(os.path.join(call,default_name))
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

