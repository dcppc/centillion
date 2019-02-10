## APIs used

To index content provided and hosted by third party
services, centillion uses API calls. API keys are 
provided in the centillion configuration file.

Currently, centillion works with the following APIs

* [Google Drive](#drive)
* [Github](#github)
* [Disqus](#disqus)

We cover more information about each below.


<a name="drive"></a>
## Google Drive

The Google Drive API is used to obtain documents from
Google Drive. We walk through the steps of setting up
the Google Drive API below.


### Creating an account

Create an account: it is important to note that when
you provide a Google Drive API key to centillion, 
centillion will index **everything that it can access**.
This means you **shoudl not** use individuals' Google
accounts to set up centillion. Instead, **create a 
dedicated Google account for your centillion instance**
and grant it access only to the items or folders that
need to be indexed.


### Enabling the API

Once you have created an account, you need to enable
the Google Drive API from the Google Cloud console.

Instructions for enabling the Google Drive API here:
<https://developers.google.com/drive/api/v3/enable-sdk>

Start by opening the Google Cloud console:
<https://console.cloud.google.com/>

In the console, create a new project for your 
centillion instance.

Once you've created your new project, you should be
on the APIs page. If not, you can always click the
three-line hamburger menu icon (top left) and pick
APIs from there.

To enable the Google Drive API from the APIs page,
click "Library" on the left side menu. Search for
Google Drive, pick the Google Drive API result,
and pick "Enable".


### Creating credentials

Once you have enabled the API, you still need to
make API keys to call the Google Drive API.
You can do this from the APIs page of the Google 
Cloud console.

To create Google Drive credentials from the APIs
page, pick "Credentials" on the left side menu.
Pick Create Credentials, then OAuth credentials.
You can add the project name to the "Consent Screen",
and leave everything else blank. When asked for
an application type, pick "Other".

Once you have done this, a temporary window showing 
your API keys will pop up. There is no need to save
this information. Click "OK" and you should see your
new credentials show up in the list.

On the right side, there is a down arrow icon.
Click this to download your OAuth API credentials.
This will download `client_secret.json`.

**IMPORTANT:** `client_secret.json` contains information
specific to the centillion OAuth application you just
created, it _does not_ give you the ability to use
the API by itself. To do that, you have to log in
using your new centillion Google account, and grant 
permission for the centillion OAuth application to 
make API calls using that account.

(Note that normally the account creating an app is 
different from the account granting permission to 
an app.)


### Converting client secret to credentials

Once the Google Drive API is enabled, you can download
`client_secrets.json`, which contains a token and a
secret token that enable you to verify you are the
true owner of the centillion OAuth application that
was just created.

To link these to an account, use the 
`scripts/prepare_gdrive.py` script in this repo
(requires the `google-api-python-client` package):

```
$ pip install --upgrade google-api-python-client

$ ls client_secrets.json
client_secrets.json

$ python scripts/prepare_gdrive.py
```

This will look for a `clients_secret.json` in the 
current directory, and will use it to 
generate a login link, which a Google
user can then visit and log in. This will then
create a `credentials.json` file, which is what
centillion needs to make real API calls.


<a name="github"></a>
## Github

There are two types of Github API credentials, used
for two different things by centillion.

First, if centillion is indexing Github content (files
or Markdown in a Github repo, or Github issues or pull
requests), it will use a Github API access token to
access information about the repository. This key
is provided in the centillion configuration file.

Second, and _independent of whether centillion is indexing
any Github content_, centillion implements an
authentication layer to limit access to authorized
users only. This authentication layer uses Github
accounts to control access (specific Github users,
organizations, or teams are whitelisted in the
centillion configuration file). This requires an
OAuth application, since users log in using their
Github account to verify their identity. The OAuth
application key and secret are provided in the
centillion configuration file.


### Creating API keys

The following instructions cover creating both types
of API credentials mentioned above. 

Before logging into Github, decide what Github account
you should use. Like with Google Drive, it is recommended
to use a dedicated Github account for your centillion
instance. The account should have access to any private
repositories that are to be indexed, and should have
the ability to view the members of a Github organization
or team, if those are used to control access.

(For example, if access to centillion is restricted to
members of the "Admins" group using centillion's access
control mechanism, the account used to create API keys
must be able to see who is in the "Admins" group!)

Start by logging into a Github account.

Click user icon in upper right and pick Settings.

Pick Developer Settings on the left side menu.

From here, you can create an API access token or
OAuth application credentials.

Copy and paste the API keys into the centillion 
config file.


<a name="disqus"></a>
## Disqus

The Disqus API takes a URL and returns a comment thread.

The [using the api](https://help.disqus.com/developer/using-the-api)
instructions at the disqus help site is a
useful place to start.

First, [create an api application](https://help.disqus.com/api/how-to-create-an-api-application)
using an account that is an owner or admin
for the Disqus forum/forums being indexed.

Once you hae an API key, you can provide it
in the centillion configuration file.

To test out the ability to list all threads in a forum
using the API, you can run the following curl command
(replacing the forum name and public API key):

```
$ curl -0 -L "https://disqus.com/api/3.0/threads/list.json?forum=<forum-name-here>&api_key=<public-api-key-here>
```

This will return json.
