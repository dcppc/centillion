#!/usr/bin/env python
import centillion

"""
Run beta centillion

https://betasearch.nihdatacommons.us

Port 5001
"""

app = centillion.webapp.get_flask_app()
app.run(port=5001,debug=False)

