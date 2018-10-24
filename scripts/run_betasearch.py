#!/usr/bin/env python
import centillion
import logging
import os

"""
Run beta centillion

https://betasearch.nihdatacommons.us

Port 5001
"""

log_dir = '/tmp/centillion'
log_file = os.path.join(log_dir,'betasearch.log')

logging.basicConfig(level=logging.INFO,
                    filename=log_file,
                    filemode='w')

app = centillion.webapp.get_flask_app()
app.run(port=5001,debug=False)

