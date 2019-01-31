#
# centillion search engine tool
# configuration file
# ------------------------------
#
# This configuration file contains configuration
# variables for the centillion search engine.s
# 
# Configuration variables are loaded by the Flask
# web server when centillion is started.
#
# Sections:
# 
#   Testing
#   Searching
#   User Interface
#   Github
#   Google Drive
#   Groups.io
#   Disqus
#   Flask


# Testing
# ========

# Turning on the DEBUG setting will print/log
# extra information about what centillion
# is doing
# NOTE: This is a Flask setting
DEBUG = False

# Turning on the TESTING setting will
# turn off Github authentication layer
TESTING = False


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





######################################
# github oauth
GITHUB_OAUTH_CLIENT_ID = "XXX"
GITHUB_OAUTH_CLIENT_SECRET = "YYY"
MATOMO_ID = 1

######################################
# github acces token
GITHUB_TOKEN = "XXX"

######################################
# groups.io
GROUPSIO_TOKEN = "XXXXX"
GROUPSIO_USERNAME = "XXXXX"
GROUPSIO_PASSWORD = "XXXXX"


# Google Drive
# =============

GOOGLE_DRIVE_ENABLED = True

# Set the path to the JSON file containing 
# client API credentials, downloaded from
# Google Cloud console. This is required to
# index Google Drive files.


# Groups.io
# =========

GROUPSIO_ENABLED = False


# Disqus
# ======

DISQUS_ENABLED = False

DISQUS_TOKEN = "XXXXX"


# Flask
# =====

# Flask secret key
SECRET_KEY = 'XXXXX'


