#!/usr/bin/env python
import centillion
import logging
import os

log_dir = '/var/log/centillion'
log_file = os.path.join(log_dir,'centillion.log')

logging.basicConfig(level=logging.INFO,
                    filename=log_file,
                    filemode='w')

CONFIG_FILE = 'config_gdrive.py'
HERE = os.path.split(os.path.abspath(__file__))[0]

app = centillion.webapp.get_flask_app(config_file=os.path.join(HERE,CONFIG_FILE))
app.run()

