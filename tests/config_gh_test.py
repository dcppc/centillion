#
# centillion search engine tool
# configuration file
# ------------------------------
#
# This configuration file contains configuration
# variables for the centillion search engine.
# 
# Configuration variables are loaded by the Flask
# web server when centillion is started.
#
# Sections:
# 
#   Access Control
#   Testing
#   Searching
#   User Interface
#   Github
#   Google Drive
#   Disqus
#   Flask


# Access Control
# ==============

# Is there a layer of access control 
# based on Github in place to protect
# this centillion instance?

# Access control whitelist:

# Pass a whitelist of Github organizations
# whose members are permitted to access
# centillion pages.
# Independent of logins and teams below.
WHITELIST_GITHUB_ORGS = []

# Pass a whitelist of Github team IDs
# whose members are permitted to access
# centillion pages.
# Team IDs are tricky to find but not hard.
# Also independent of the orgs listed above.
WHITELIST_GITHUB_TEAMS = []

# Pass a whitelist of Github logins
# (usernames) of users who are permitted
# to access centillion pages.
# Independent of orgs and teams above.
WHITELIST_GITHUB_LOGINS = []


# Admin whitelist:

# Pass a whitelist of admin Github organizations
# whose members are permitted to access
# the centillion control panel/admin pages.
# Independent of logins and teams below.
ADMIN_WHITELIST_GITHUB_ORGS = []

# Pass a whitelist of admin Github team IDs
# whose members are permitted to access
# the centillion control panel/admin pages.
# Team IDs are tricky to find but not hard.
# Also independent of the orgs listed above.
ADMIN_WHITELIST_GITHUB_TEAMS = []

# Pass a whitelist of admin Github logins
# (usernames) of users who are permitted
# to access control panel/admin pages.
# Independent of orgs and teams above.
ADMIN_WHITELIST_GITHUB_LOGINS = []


# Testing
# ========

# Turning on the DEBUG setting will...?
# NOTE: This is a Flask setting
DEBUG = False

# If true, this will populate the centillion search index
# with a pile of fake documents. If this is true,
# all API credentials are ignored.
# (This is extremely useful for testing without the
# hassle of APIs.)
FAKEDOCS = False


# Searching
# ==========

# Set the on-disk location of the search
# index (relative path)
INDEX_DIR = "test_search_index_gh"


# User Interface
# ==============

# This is the tagline that appears below the
# centillion logo on all centillion pages
TAGLINE = "the document search engine"

# Customize the organization, name, and URL
# of the centillion Github repo in the footer
FOOTER_REPO_ORG = "dcppc"
FOOTER_REPO_NAME = "centillion"

# When someone runs a search on centillion, 
# centillion (under the hood, whoosh) parses the
# query string. If this setting is true, it shows
# the user the full parsed query
# NOTE: This is usually more confusing than helpful,
# but can be useful for debugging
SHOW_PARSED_QUERY = False


# Github
# ======

GITHUB_ENABLED = True

# To access documents in various repositories,
# a Github API access token is used.
from secrets import GITHUB_TOKEN

## If you have enabled a Github authentication layer,
## you must create a Github OAuth application, and
## obtain a client ID and client secret for your
## centillion instance.
#from secrets import GITHUB_OAUTH_CLIENT_ID
#from secrets import GITHUB_OAUTH_CLIENT_SECRET

# Flag to indicate whether to truncate the
# list of a repo's issues/PRs processed.
# This is mainly useful for testing.
TRUNCATE_ISSUES_LISTING = False

REPOSITORIES = [
        "charlesreid1/centillion-search-demo"
]


# Google Drive
# =============

GOOGLE_DRIVE_ENABLED = False



# Disqus
# ======

DISQUS_ENABLED = False


# Flask
# =====

# Flask secret key 
# (should be a random string, this is
# used to establish sessions with users)
from secrets import SECRET_KEY

