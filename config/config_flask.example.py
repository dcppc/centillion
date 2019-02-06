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
FAKEDOCS = True


# Searching
# ==========

# Set the on-disk location of the search
# index (relative path)
INDEX_DIR = "search_index"


# User Interface
# ==============

# This is the tagline that appears below the
# centillion logo on all centillion pages
TAGLINE = "Search the Data Commons"

# Customize the organization, name, and URL
# of the centillion Github repo in the footer
FOOTER_REPO_ORG = "dcppc"
FOOTER_REPO_NAME = "centillion"
FOOTER_REPO_URL = "https://github.com/dcppc/centillion"

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

# Set the API keys for the Github API.
# These are obtained from Github Account Settings.
# These are required to index Github issues and files.
GITHUB_OAUTH_CLIENT_ID = "XXX"
GITHUB_OAUTH_CLIENT_SECRET = "YYY"

# Alternatively, a Github access token
# can be used
#GITHUB_TOKEN = "XXXXX"

# Flag to indicate whether to truncate the
# list of a repo's issues/PRs processed.
# This is mainly useful for testing.
TRUNCATE_ISSUES_LISTING = False

REPOSITORIES = [
        "dcppc/documentation-archive",
        "dcppc/organize",
        "dcppc/apis",
        "dcppc/data-stewards",
        "dcppc/dcppc-phase1-demos",
        "dcppc/dcppc-deliverables",
        "dcppc/dcppc-bot",
        "dcppc/guids",
        "dcppc/dcppc.github.io",
        "dcppc/test-dcppc-deliverables",
        "dcppc/crosscut-metadata",
        "dcppc/project-management",
        "dcppc/dcppc-milestones",
        "dcppc/dcppc-workshops",
        "dcppc/2018-may-workshop",
        "dcppc/internal",
        "dcppc/private-www",
        "dcppc/full-stacks",
        "dcppc/2018-june-workshop",
        "dcppc/2018-july-workshop",
        "dcppc/metadata-matrix",
        "dcppc/design-guidelines",
        "dcppc/design-guidelines-discuss",
        "dcppc/lucky-penny",
        "dcppc/2018-august-workshop",
        "dcppc/2018-september-workshop",
        "dcppc/nih-demo-meetings",
        "dcppc/markdown-issues",
        "dcppc/2018-paper-dcppc",
        "dcppc/centillion",
        "dcppc/public-www",
        "dcppc/uncle-archie",
        "dcppc/use-case-library",
        "dcppc/sodium-documentation",
        "dcppc/calendars",
        "dcppc/data-access",
        "dcppc/four-year-plan",
        "dcppc/2018-oct-workshop",
        "dcppc/cloud-guidebook",
]


# Google Drive
# =============

GOOGLE_DRIVE_ENABLED = True

# Set the path to the JSON file containing 
# client API credentials, downloaded from
# Google Cloud console. This is required to
# index Google Drive files.


# Flag to indicate whether to truncate the
# list of documents processed from Google Drive.
# This is mainly useful for testing.
TRUNCATE_DRIVE_LISTING = False


# Disqus
# ======

DISQUS_ENABLED = False

# Disqus API token
DISQUS_TOKEN = "XXXXX"


# Flask
# =====

# Flask secret key 
# (should be a random string, this is
# used to establish sessions with users)
SECRET_KEY = 'XXXXX'

