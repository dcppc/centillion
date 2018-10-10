from setuptools import setup

"""
setup.py for centillion

search engine tool
"""

with open('requirements.txt') as f:
    required = [x for x in f.read().splitlines() if not x.startswith("#")]

from src import __version__

config = {
    'name': 'centillion',
    'description': 'centillion is a home-brewed search engine tool',
    'url': 'https://github.com/dcppc/centillion',
    'author': 'Charles Reid',
    'version' : __version__,
    'install_requires': required,
    'include_package_data' : True,
    'test_suite': 'nose.collector',
    'tests_require': ['nose'],
    'packages': [
        'centillion',
        'centillion.webapp',
        'centillion.search',
    ],
    'package_dir' : {
        'centillion' :        'src',
        'centillion.webapp' : 'src/webapp',
        'centillion.search' : 'src/search',
    },
    'scripts': [],
    'zip_safe' : False
}

setup(**config)
