## Quick start: using centillion

Also see [Quick Start](quickstart.md).

To use centillion, start with a Python script that will import
centillion, create an instance of the webapp, set any custom
configuration variables, and run the webapp. For example,
the following script is in `examples/run_centillion.py`:

```python
import centillion

app = centillion.webapp.get_flask_app()

app.config['TESTING'] = True

app.run()
```

When this script is run, centillion will also look for a configuration
file containing all of the keys and settings that centillion needs to run.
This can be provided using the `CENTILLION_CONFIG` variable:

```bash
CENTILLION_CONFIG="conf/config_flask.py" python examples/run_centillion.py
```

