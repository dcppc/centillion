# Table of Contents

*   [Centillion Quality Engineering Plan](#centillion-quality-engineering-plan)
    *   [Summary](#summary)
    *   [Tracking Bugs and Issues](#tracking-bugs-and-issues)
    *   [Branches, Versioning, and Git Workflow](#branches-versioning-and-git-workflow)
    *   [Communication and Mailing Lists](#communication-and-mailing-lists)
    *   [Checklists](#checklists)
    *   [Documentation](#documentation)
    *   [Configuration Management Tools](#configuration-management-tools)
    *   [Tests](#tests)
    *   [Code Reviews](#code-reviews)
    *   [Formal Release Process](#formal-release-process)
    *   [Continual Process Improvement](#continual-process-improvement)

Centillion Quality Engineering Plan
===================================

Summary
-------

This document contains a quality engineering plan for centillion, the
Data Commons search engine.

Tracking Bugs and Issues
------------------------

We utilize the [issues
section](https://github.com/dcppc/centillion/issues) of the centillion
repository to keep track of bugs and feature requests.

Branches, Versioning, and Git Workflow
--------------------------------------

All code is kept under version control in the
[dcppc/centillion](https://github.com/dcppc/centillion) Github
repository.

**Primary Git Branches:**

We utillize a git branch pattern that has two primary branches: a
development branch and a stable branch.

-   The primary **development branch** is `dcppc` and is actively
    developed and deployed to <https://betasearch.nihdatacommons.us>.

-   The primary **stable branch** is `releases/v1` and is stable and
    deployed to <https://search.nihdatacommons.us>.

All tagged versions of Centillion exist on the stable branch. Only
tagged versions of centillion are run on
<https://search.nihdatacommons.us>.

**Other Branches:**

Features are developed by creating a new branch from `dcppc`, working on
the feature, and opening a pull request. When the pull request is
approved, it can be merged into the `dcppc` branch.

When features have accumulated and a new version is ready, a new
pre-release branch will be made to prepare for a new release. When the
pre-release branch is ready, it is merged into the stable branch in a
single merge commit and a new version of centillion is tagged. The new
version is deployed on <https://search.nihdatacommons.us>.

Commits to fix bugs (hotfixes) may need to be applied to both the stable
and development branches. In this case, a hotfix branch should be
created from the head commit of the stable branch, and the appropriate
changes should be made on the branch. A pull request should be opened to
merge the hotfix into the release branch. A second pull request should
be opened to merge the hotfix into the development branch. Once the
hotfix is merged into the stable branch, a new version should be tagged.

Communication and Mailing Lists
-------------------------------

-   No mailing list currently exists for centillion.

-   Github issues are the primary form of communication about
    development of centillion. This is the best method for communicating
    bug reports or detailed information.

-   The Send Feedback button on the centillion page is the primary way
    of getting quick feedback from users about the search engine.

-   The [\#centillion](https://nih-dcppc.slack.com/messages/CCD64QD6G)
    Slack channel in the DCPPC slack workspace is the best place for
    conversations about centillion (providing feedback, answering quick
    questions, etc.)

Checklists
----------

We plan to utilize the Wiki feature of the Github repository to develop
checlists:

-   Checklist for releases
-   Checklist for deployment of https://search.nihdatacommons.us nginx
    etc.

Documentation
-------------

The documentation is a pile of markdown documents, turned into a static
site using mkdocs.

Configuration Management Tools
------------------------------

We do not currently utilize any configuration management software,
because centillion is not packaged as an importable Python module.

Packaging centillion is a future goal that is closely related to the
need to improve and modularize the internal search schema/document type
abstraction. These improvements would allow the types of collections
being indexed to be separated from "core centillion", and core
centillion would be packaged.

Tests
-----

See (ref) for a full test plan with more detail.

Summary of test plan:

-   Implement tests for the four major pages/components
    -   Login/authentication
    -   Search
    -   Master List
    -   Control Panel
-   Test authentication with two bot accounts (yammasnake and florence
    python)

-   Separate frontend and backend tests

-   Add a test flag in the flask config file to change the backend
    behavior of the server

Code Reviews
------------

CI tests will be implemented for all pull requests.

Pull requests to the **stable branch** have the following checks in
place:

-   PRs to the stable branch require at least 1 PR review
-   PRs to the stable branch must pass CI tests

Pull requests to the **development branch** have the following checks in
place:

-   PRs to the development branch must pass CI tests

Formal Release Process
----------------------

In order to ensure a stable, consistent product, we utilize the
branching pattern described above to implement new features in the
development branch and test them out on
<https://betasearch.nihdatacommons.us>.

Once features and bug fixes have been tested and reviewed internally,
they are ready to be deployed. A new pre-release branch is created from
the development branch. The pre-release branch has a feature freeze in
place. Changes are made to the pre-release branch to prepare it for the
next major version release.

When the pre-release branch is finished, it is merged into the stable
branch. The head commit of the stable version is tagged with the lastest
release number.

Finally, the new version is deployed on
<https://search.nihdatacommons.us>.

Continual Process Improvement
-----------------------------

We will utilize the centillion wiki on Github to keep track of repeated
processes and opportunities for improvement. Feedback and ideas for
process improvement can also be submitted via Github issues.
