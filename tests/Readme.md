Centillion Tests
================

Table of Contents
------------------

*   [Centillion Tests](#centillion-tests)
    *   [Test Plan](#test-plan)
        *   [Local Tests](#local-tests)
        *   [Short Tests](#short-tests)
        *   [Long Tests](#long-tests)
    *   [Credentials](#credentials)
    *   [Detailed Description of Tests](#detailed-description-of-tests)
        *   [Authentication Layer Tests](#authentication-layer-tests)
        *   [Search Function Tests](#search-function-tests)
        *   [Master List Endpoint Tests](#master-list-endpoint-tests)
        *   [Control Panel Endpoint Tests](#control-panel-endpoint-tests)
        *   [Continuous Integration Plan](#continuous-integration-plan)
    *   [Procedure/Checklist](#procedurechecklist)


Test Plan
---------

The test suite for centillion needs to check each of the major
components of centillion, as well as check the authentication mechanism
using multiple login credentials.

We implement the following checks:

1.  Check authentication mechanism(s) (yamasnake and florence python)

2.  Check search function

3.  Check master list endpoint

4.  Check control panel endpoint

5.  Check update search index endpoints

The tests are written such that the back end and front end are tested
separately.

We need also need different tiers of tests, so we don't max out API
calls by making lots of commits to multiple PRs.

We have two types of tests:

* Backend tests - check the core functionality of centillion and its functions
* Frontend tests - check the functionality of the user interface

We have three tiers of tests: 

* Local tests - quick tests for CI, no API calls 
* Short tests - tests using dummy API accounts 
* Long tests - tests using DCPPC API accounts

### Local Tests

Local tests can be run locally without any interaction with APIs. These
will still utilize centillion's search schema, but will load the search
index with fake documents rather than fetching them from an API.

Uncle Archie, which runs CI tests, runs local tests only (unless you
request it to run short test or long test.)

### Short Tests

Short tests utilize credentials for bot accounts that have intentionally
been set up to have a "known" corpus of test documents. These would
provide unit-style tests for centillion - are the mechanics of indexing
a particular type of document from a particular API working?

### Long Tests

Long tests are indexing the real deal, utilizing the credentials used in
the final production centillion. This test takes longer but is more
likely to catch corner cases specific to the DCPPC documents.

Credentials
-----------

Running tests on centillion requires multiple sets of credentials. Let's
lay out what is needed:

-   The Flask app requires a token/secret token API key pair to allow
    users to authenticate through Github and confirm they are members of
    the DCPPC organization. This OAuth application is owned by Charles
    Reid (@charlesreid1).

-   The search index needs a Github access token so that it can
    interface with the Github API to index files and issues. This access
    token is specified (along with other secrets) in the Flask
    configuration file. The access key comes from Florence Python
    (@fp9695253).

-   The search index also requires a Google Drive API access token. This
    must be an access token for a user who has authenticated with the
    Centillion Google Drive OAuth application. This access token comes
    from <mailroom@nihdatacommons.com>.

-   The search index requires API credentials for any other APIs
    associated with other document collections (Groups.io, Hypothesis,
    Disqus).

-   The backend test requires the credentials provided to Flask.

-   The frontend test (Selenium) needs two Github username/passwords:
    one for Florence Python (@fp9695253) and one for Yamma Snake
    (@yammasnake). These are required to simulate the user
    authenticating with Github through the browser.
    -   The frontend test credentials are a special case.
    -   The frontend tests expect credentials to come from environment
        variables.
    -   These environment variables get passed in at test time.
    -   Tests are all run on [Uncle Archie](https://github.com/dcppc/uncle-archie).
    -   Uncle Archie already has to protect a confidential config file
        containing Github credentials, so add additional credentials for
        frontend tests there.
    -   Logical separation: these credentials are not needed to
        *operate* centillion, these credentials are needed to *test*
        centillion
    -   Uncle Archie already requires github credentials, already
        protects sensitive info.
    -   Google Drive requiring its own credentials file on disk is a
        pain.

In summary: tests use the `config_flask.py` and `config_centillion.py`
files to provide it with the API keys it needs and to instruct it on
what to index. The credentials and config files will control what the
search index will actually index. The Uncle Archie CI tester config file
contains the credentials needed to run frontend tests (check the
login/authentication layer).

Detailed Description of Tests
-----------------------------

### Authentication Layer Tests

Frontend tests run as Florence Python:

-   Can we log in via github and reach centillion
-   Can we reach the control panel

Frontend tests run as Yamma Snake (DCPPC member):

-   Can we log in via github and reach centillion
-   Can we reach the control panel

### Search Function Tests

Frontend tests:

-   Can we enter something into search box and submit
-   Can we sort the results
-   Do the results look okay

Backend tests:

-   Load the search index and run a query using whoosh API

### Master List Endpoint Tests

Frontend tests:

-   Can we get to the master list page
-   Can we sort the results
-   Do the results look okay

Backend tests:

-   Check the output of the `/list` API endpoint

### Control Panel Endpoint Tests

Frontend tests:

-   Can we get to the control panel page
-   Can we click the button to trigger an indexing event

Backend tests:

-   Trigger a re-index of the search index from the backend.


Test Automation and Infrastructure
---------------------------------------

The [Quality Engineering plan](../quality/Readme.md) contains
additional information about the infrastructure that will be
put into place to ensure code quality, but one important part
of that is automation of testing.

[Uncle Archie](https://github.com/dcppc/uncle-archie) is the 
continuous integration service that will run tests on every 
pull request to the centillion repo.


