from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os


"""
Convenience class wrapper for Google Drive OAuth.

This requires that the user download credentials.json
from Google Cloud Console (API section).

The user should set client_secret_file to that JSON file,
probably named client_secret.json, that contains the 
application's public and private authentication token. 
These tokens are APPLICATION specific.

The authentication process uses these credentials to ask for
an OAuth token on behalf of the user. This step requires the
user to log in, and when they do it creates credentials.json.
These contain the credentials to perform actions as the user
that just logged in/granted permission to your app.
"""


class GDrive(object):
    def __init__(self,config):
        """
        Set up the Google Drive API instance.
        Create the API instance here, hand it over in get_service().
        """
        default_credentials_file = 'credentials.json'
        default_client_file = 'client_secrets.json'

        # GOOGLE_DRIVE_CREDENTIALS env var takes priority
        if 'GOOGLE_DRIVE_CREDENTIALS' in os.environ:
            self.credentials_file = os.environ['GOOGLE_DRIVE_CREDENTIALS']
            if not os.path.exists(self.credentials_file):
                err = "ERROR: Missing credentials file specified by GOOGLE_DRIVE_CREDENTIALS "
                err += "environment variable: %s"%(self.credentials_file)
                raise Exception(err)

        # GOOGLE_DRIVE_CREDENTIALS config var takes second priority
        elif 'GOOGLE_DRIVE_CREDENTIALS' in config:
            self.credentials_file = config['GOOGLE_DRIVE_CREDENTIALS']
            if not os.path.exists(self.credentials_file):
                err = "ERROR: Missing credentials file specified by GOOGLE_DRIVE_CREDENTIALS "
                err += "in centillion config file: %s"%(self.credentials_file)
                raise Exception(err)

        # hail mary: look for credentials.json
        elif os.path.exists(default_credentials_file):
            self.credentials_file = default_credentials_file

        # halfway there: client_secrets.json
        elif os.path.exists(default_client_file):
            err = "ERROR: Missing credentials file, only 'client_secrets.json' found. "
            err += "The 'client_secrets.json' file is for the OAuth application only, "
            err += "you must use 'client_secrets.json' to authenticate a Google account "
            err += "with the Google Drive API. See the scripts folder."
            raise Exception(err)

        else:
            err = "ERROR: Missing credentials file, no 'credentials.json' found."
            raise Exception(err)

        # Setup the Drive v3 API
        self.SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
        self.store = file.Storage(self.credentials_file)

    def get_service(self):
        """
        Return an instance of the Google Drive API service.
        """

        creds = self.store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(self.client_secret_file, self.SCOPES)
            creds = tools.run_flow(flow, self.store)

        service = build('drive', 'v3', http=creds.authorize(Http()))
        return service

if __name__=="__main__":
    g = GDrive()
    s = g.get_service()
