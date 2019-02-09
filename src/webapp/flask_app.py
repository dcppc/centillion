from .const import base, call, DEFAULT_CONFIG

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

NOTE: to load a Python file as a Flask config file,
use the flask app's built-in config.from_pyfile() method:

>>> app.config.from_pyfile("my_config_file.py")
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
        # Pop config_file keyword argument
        # before calling flask app constructor,
        # since this is the only non-flask parameter
        if 'config_file' in kwargs.keys():
            config_file = kwargs['config_file']
            del kwargs['config_file']

        super().__init__(*args,**kwargs)

        # ----------------------------
        # Load config file
        msg = "CentillionFlask: __init__(): Preparing to load webapp config file."
        logging.info(msg)
        loaded_config = False

        # Flask Config 
        # ------------
        # We have 4 ways to pass a Flask config to centillion.
        # 
        # Option 1: set the `CONFIG_CENTILLION` env var
        # Option 2A: specify the relative or absolute path to a config file when initializing flask app
        # Option 2B: have a config file (with name specified by DEFAULT_CONFIG on const.py) in the current directory
        # Option 3: have a config file (wth name specified by DEFAULT_CONFIG in const.py) in `~/.config/centillion/`
        # 
        # (Option 2A and 2B are the same, but one specifies
        # the config file name and one uses the default.)


        cf = 'CENTILLION_CONFIG'
        if cf in os.environ:

            # Option 1:
            # 
            # The user can set the centillion config file
            # using the CENTILLION_CONFIG environment var
            # when they run their centillion driver program.

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

            msg = "CentillionFlask: __init__(): Did not find CENTILLION_CONFIG environment variable. Still looking for config file...\n"
            logging.info(msg)

            # Option 2:
            # 
            # User specifies the name of a config file,
            # either relative or absolute, when they
            # create the Flask app.
            # 
            # Note: if config_file = DEFAULT_CONFIG,
            # this is Option 2B.
            # 
            cwd_config = os.path.join(call,config_file)
            if os.path.isfile(cwd_config):
                self.config.from_pyfile(cwd_config)
                loaded_config = True
                msg = "CentillionFlask: __init__(): Succesfuly loaded user-specified config file\n"
                msg += "Loaded config file at %s"%(cwd_config)
                logging.info(msg)

            elif os.path.isfile(config_file):
                self.config.from_pyfile(config_file)
                loaded_config = True
                msg = "CentillionFlask: __init__(): Succesfuly loaded user-specified config file\n"
                msg += "Loaded config file at %s"%(config_file)
                logging.info(msg)

            else:

                msg = "CentillionFlask: __init__(): Did not find config file anywhere, punting and looking for ~/.config/centillion/%s\n"%(DEFAULT_CONFIG)
                logging.info(msg)

                # Option 3:
                # 
                # User must have a config file in 
                # ~/.config/centillion/$DEFAULT_CONFIG
                # 
                home = str(Path.home())
                home_config = os.path.join(home,'.config','centillion',DEFAULT_CONFIG)
                if os.path.isfile(home_config):
                    self.config.from_pyfile(home_config)
                    loaded_config = True
                    msg = "CentillionFlask: __init__(): Succesfuly loaded config file in home directory\n"
                    msg += "Loaded config file at %s"%(home_config)
                    logging.info(msg)


        if not loaded_config:
            err = "ERROR: CentillionFlask: __init__(): Problem setting config file. Check that %s exists or that the %s environment variable is set!\n"%(config_file,cf)
            logging.exception(err)
            raise Exception(err)

        self.validate_config()



    def validate_config(self):
        """
        Perform validation of the configuration file.
        Check for required keys, invalid conditions,
        or other weirdness.
        """
        config = self.config

        # which doc types are enabled
        need_at_least_one = ['GOOGLE_DRIVE_ENABLED','GITHUB_ENABLED','DISQUS_ENABLED']
        found_one = False
        for n in need_at_least_one:
            if n in config.keys():
                found_one = True
                break
        if not found_one:
            raise Exception("Error: need at least one of: %s"%(", ".join(need_at_least_one)))

        if 'GOOGLE_DRIVE_ENABLED' in config.keys():
            if config['GOOGLE_DRIVE_ENABLED']:
                if 'GOOGLE_DRIVE_CREDENTIALS_FILE' in config.keys():
                    if os.path.basename(config['GOOGLE_DRIVE_CREDENTIALS_FILE']) != 'credentials.json':
                        raise Exception("Error: the file specified with GOOGLE_DRIVE_CREDENTIALS_FILE in the config file must have a filename of 'credentials.json'")


