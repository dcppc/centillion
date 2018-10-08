from .flask_app import CentillionFlask
from .flask_routes import setup_routes
from .const import base

from flask import Flask, request, abort, render_template
import os


def get_flask_app():
    """
    This utility function is how we create the
    Flask app from our driver.
    """
    app = CentillionFlask(
            __name__,
            template_folder = os.path.join(base,'templates'),
            static_folder = os.path.join(base,'static')
    )
    setup_routes(app)
    return app

