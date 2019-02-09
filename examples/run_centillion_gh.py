import centillion

app = centillion.webapp.get_flask_app(config_file='../config/config_centillion_gh.py')
app.run()
