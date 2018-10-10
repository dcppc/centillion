import os
import requests

"""
Generate Groups.io API Token

This script uses your username and password to authenticate
with the Groups.io API and obtain a secret API key.

Set your Groups.io password using an environment variable:

    $ GROUPSIO_PASSWORD="mydumbpassword" python generate_groupsio_api_token.py

"""

mypassword = os.environ['GROUPSIO_PASSWORD']

data = [
        ('email', 'charlesreid1.dib@gmail.com'),
        ('password', mypassword),
]

response = requests.post('https://api.groups.io/v1/login', data=data, auth=('123456', ''))

print(response.json())

