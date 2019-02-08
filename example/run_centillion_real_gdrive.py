import centillion
import os

CONFIG_FILE = 'config_gdrive.py'
HERE = os.path.split(os.path.abspath(__file__))[0]

app = centillion.webapp.get_flask_app(config_file=os.path.join(HERE,CONFIG_FILE))

app.run()

