from .flask_app import CentillionFlask
from .flask_routes import setup_routes
from .const import base, DEFAULT_CONFIG

from flask import Flask, request, abort, render_template
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

def get_flask_app(config_file=DEFAULT_CONFIG):
    """
    This utility function is how we create the
    Flask app from our driver.
    """
    app = CentillionFlask(
            __name__,
            config_file = config_file,
            template_folder = os.path.join(base,'templates'),
            static_folder = os.path.join(base,'static')
    )
    setup_routes(app)
    return app

