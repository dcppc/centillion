from gdrive_util import GDrive

"""
Auth for The Centillion

This ensures we have auth set up correctly.
Checks two APIs:
    - Github API (check GITHUB_TOKEN env var)
    - Google Drive (check for `credentials.json` or
      go through oauth process)
"""

# Quick test of github access token
g = Github(gh_access_token)
org = g.get_organization('dcppc')

gd = GDrive()
service = gd.get_service()

