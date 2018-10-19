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
    def __init__(self,
                 credentials_file = 'credentials.json',
                 client_secret_file = 'client_secret.json'
    ):
        """
        Set up the Google Drive API instance.
        Create the API instance here, hand it over in get_service().
        """
        self.credentials_file = credentials_file
        self.client_secret_file = client_secret_file

        if os.path.exists(credentials_file) is False:
            if os.path.exists(client_secret_file) is False:
                err = "ERROR: Could not find Google Drive credentials files: "
                err += "missing credentials file %s "%(self.credentials_file)
                err += "or a client secret file %s "%(client_secret_file)
                raise Exception(err)

        # Setup the Drive v3 API
        self.SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
        self.store = file.Storage(credentials_file)

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
