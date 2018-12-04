#!/usr/bin/env python
import os
import re

x_y_z = '1.7.3'

"""
Release Prep Script

This script prepares the code base for a release of version X.Y.Z

It does this by editing files referencing the version number,
and replacing the existing version with the new version.

Readme.md
docs/index.md
src/__init__.py
src/webapp/templates/footer.html
"""


# ---------------------------------------
# Set up directories
scripts_dir = os.path.dirname(os.path.abspath(__file__))
repo_dir =  os.path.join(scripts_dir,'..')
src_dir = os.path.join(scripts_dir,'..','src')


# ---------------------------------------
# replace_func
def replace(which_file,replace_this,with_this):

    print("Reading file %s"%(which_file))
    with open(which_file,'r') as f:
        content = f.read()
    
    print("Replacing version number...")
    content2 = re.sub(replace_this,with_this,content)
    
    print("Writing %s"%(which_file))
    with open(which_file,'w') as f:
        f.write(content2)

def replace_version(which_file):
    replace(which_file,r'version-\d\.\d\.\d','version-%s'%(x_y_z))

def replace_init_version(which_file):
    replace(which_file,r'version__="\d\.\d\.\d"','version__="%s"'%(x_y_z))

def replace_foot_version(which_file):
    replace(which_file,r'version \d\.\d\.\d','version %s'%(x_y_z))

# ---------------------------------------
# Readme.md
readme_file = os.path.join(repo_dir,'Readme.md')

if not os.path.exists(readme_file):
    raise Exception("Error: no readme file %s found"%(readme_file))

replace_version(readme_file)


# ---------------------------------------
# docs/index.md
index_file = os.path.join(repo_dir,'docs','index.md')

if not os.path.exists(index_file):
    raise Exception("Error: no index file %s found"%(index_file))

replace_version(index_file)


# ---------------------------------------
# src/__init__.py
init_file = os.path.join(repo_dir,'src','__init__.py')

if not os.path.exists(init_file):
    raise Exception("Error: no init file %s found"%(init_file))

replace_init_version(init_file)


# ---------------------------------------
# src/webapp/templates/footer.html
foot_file = os.path.join(repo_dir,'src','webapp','templates','footer.html')

if not os.path.exists(foot_file):
    raise Exception("Error: no footer file %s found"%(foot_file))

replace_foot_version(foot_file)

