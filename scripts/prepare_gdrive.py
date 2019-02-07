from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os


"""
Prepare GOogle Drive

This script turns client_secret.json -> credentials.json.

client_secret.json is provided by Google when you
enable the Google Drive API and create an OAuth
application. It contains your OAuth application's
credentials only.

credentials.json is required by centillion to
call the Google Drive API. These credentials are
for a Google account and require a login step.

This application uses client_secret.json to create
an OAuth login link. Open this link and log in
using the account centillion will use.

When you are finished you will have a credentials.json
file.
"""

class GDrive(object):
    def __init__(self):
        """
        Set up the Google Drive API instance.
        Create the API instance here, hand it over in get_service().
        """
        self.client_secret_file = 'client_secret.json'
        self.credentials_file = 'credentials.json'

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
