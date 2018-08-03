import requests
from github import Github
import os, re
import base64
from datetime import datetime, timedelta

"""
Walk a Repo's File Tree

This walks through every file in a repository
and looks for files matching a particular
criteria (file extension).
"""

# -----------------------------------
# USER SHOULD CHANGE THESE PARAMETERS
REPOS_LIST = ["dcppc/2018-june-workshop",
              "dcppc/2018-july-workshop",
              "dcppc/2018-august-workshop",
              "dcppc/data-stewards"]
EXT = '.md'
# -----------------------------------


def main():

    for which_repo in REPOS_LIST:
        find_files_with_extension(which_repo)


def find_files_with_extension(reponame):
    """
    Find files that match the given criteria
    (extension matching EXT) and then do 
    something boring with them.
    """

    if '/' not in reponame:
        err = "No slash in repository name provided: %s\n"%(reponame)
        err += "Provide repo names the format org-name/repo-name"
        raise Exception(err)

    which_org, which_repo = re.split('/',reponame)

    print("-"*40)
    print("Now scanning repository %s for markdown files."%(reponame))

    access_token = os.environ['GITHUB_TOKEN']

    # Github -> get organization -> get repository
    g = Github(access_token)
    org = g.get_organization(which_org)
    repo = org.get_repo(which_repo)

    # Get head commit
    commits = repo.get_commits()
    last = commits[0]
    sha = last.sha

    # Get all the docs
    tree = repo.get_git_tree(sha=sha, recursive=True)
    docs = tree.raw_data['tree']

    count = 0
    total = len(docs)
    for d in docs:
        # For each doc, get the file extension
        # If it matches EXT, download the file
        fpath = d['path']
        furl = d['url']
        _, fname = os.path.split(fpath)
        _, fext = os.path.splitext(fpath)
        if fext==EXT:

            # Increment document counter
            count += 1

            # Unpack the requests response and decode the content
            response = requests.get(furl)
            jresponse = response.json()
            try:
                binary_content = re.sub('\n','',jresponse['content'])
                content = base64.b64decode(binary_content)
                print("File %s has %s characters"%(fpath, len(content)))
            except KeyError:
                print("ERROR! Could not extract 'content' field. You probably hit the rate limit.")

    print("Finished scanning repository %s, found %d markdown files, %d total files."%(reponame,count,total))
    print("-"*40)
    print("\n")


if __name__=="__main__":
    main()

