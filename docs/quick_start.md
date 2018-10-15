## Quickstart (With Github Auth)

Start by creating a Github OAuth application.
Get the public and private application key 
(client token and client secret token)
from the Github application's page.
You will also need a Github access token
(in addition to the app tokens).

When you create the application, set the callback
URL to `/login/github/authorized`, as in:

```
https://<url>/login/github/authorized
```

Edit the Flask configuration `config_flask.py`
and set the public and private application keys.

Now run centillion:

```
python centillion.py
```

or if you used http instead of https:

```
OAUTHLIB_INSECURE_TRANSPORT="true" python centillion.py
```

This will start a Flask server, and you can view the minimal search engine
interface in your browser at `http://<ip>:5000`.


## Troubleshooting

If you are having problems with your callback URL being treated
as HTTP by Github, even though there is an HTTPS address, and
everything else seems fine, try deleting the Github OAuth app
and creating a new one.


