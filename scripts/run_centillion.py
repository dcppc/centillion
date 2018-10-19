#!/usr/bin/env python
import centillion

"""
Run centillion

https://search.nihdatacommons.us

Port 5000
"""

app = centillion.webapp.get_flask_app()
app.run(port=5000,debug=False)

