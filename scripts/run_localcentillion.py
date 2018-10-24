#!/usr/bin/env python
import centillion
import os


"""
Run centillion

https://search.nihdatacommons.us

Port 5000
"""


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = centillion.webapp.get_flask_app()
app.run(port=5000)

