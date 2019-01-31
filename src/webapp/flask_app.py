from .const import base, call

from flask import Flask, request, abort, render_template
import os, sys
import json
import logging
from pathlib import Path


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

        # Flask Config 
        # ------------
        # We have 3 ways to pass a Flask config to centillion.
        # 
        # Option 1: set the `CONFIG_CENTILLION` env var
        # Option 2 (lazy): have a `config_flask.py` in the current directory
        # Option 3 (lazy): have a `config_flask.py` in `~/.config/centillion/config_flask.py`

        # Option 1:
        # The user can set the centillion config file
        # using the CENTILLION_CONFIG environment var
        # when they run their centillion driver program.
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
            default_name = 'config_flask.py'

            # Option 2 (lazy):
            # The user can be lazy and not specify `CONFIG_CENTILLION`,
            # but then they must have a file named `config_flask.py`
            # in the current working directory (this option)
            # or in ~/.config/centillion/config_flask.py (next option)
            cwd_config = os.path.join(call,default_name)
            if os.path.isfile(cwd_config):
                self.config.from_pyfile(cwd_config)
                loaded_config = True
                msg = "CentillionFlask: __init__(): Succesfuly loaded webapp config file found in current directory\n"
                msg += "Loaded config file at %s"%(cwd_config)
                logging.info(msg)


            # Option 3 (lazy):
            # The user can be lazy and not specify CONFIG_CENTILLION,
            # but then they must have a file named config_flask.py
            # in the current working directory (prior option)
            # or in ~/.config/centillion/config_flask.py (this option)
            home = str(Path.home())
            home_config = os.path.join(home,'.config','centillion',default_name)
            if os.path.isfile(home_config):
                self.config.from_pyfile(home_config)
                loaded_config = True
                msg = "CentillionFlask: __init__(): Succesfuly loaded webapp config file in home directory\n"
                msg += "Loaded config file at %s"%(home_config)
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

