#!/usr/bin/env python
import centillion
import logging
import os


"""
Run centillion

https://search.nihdatacommons.us

Port 5000
"""

#os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

log_dir = '/tmp/centillion'
log_file = os.path.join(log_dir,'localcentillion.log')

logging.basicConfig(level=logging.INFO,
                    filename=log_file,
                    filemode='w')

app = centillion.webapp.get_flask_app()
app.run(port=5000)

