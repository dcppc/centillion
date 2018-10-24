#!/usr/bin/env python
import centillion
import logging
import os

"""
Run centillion

https://search.nihdatacommons.us

Port 5000
"""

log_dir = '/tmp/centillion'
log_file = os.path.join(log_dir,'centillion.log')

logging.basicConfig(level=logging.INFO,
                    filename=log_file,
                    filemode='w')

app = centillion.webapp.get_flask_app()
app.run(port=5000,debug=False)

