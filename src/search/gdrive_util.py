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
    def __init__(self, gdrive_token_path, config):
        """
        Set up the Google Drive API instance.
        Create the API instance here, hand it over in get_service().
        """
        # Setup the Drive v3 API
        self.SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
        self.store = file.Storage(gdrive_token_path)

    def get_service(self):
        """
        Return an instance of the Google Drive API service.
        """
        creds = self.store.get()
        if not creds or creds.invalid:
            raise Exception("Error: invalid or missing Google Drive API credentials")

        service = build('drive', 'v3', http=creds.authorize(Http()))
        return service

if __name__=="__main__":
    g = GDrive()
    s = g.get_service()
