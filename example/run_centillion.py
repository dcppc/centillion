import centillion

app = centillion.webapp.get_flask_app()

app.config['TESTING'] = True

app.run()

