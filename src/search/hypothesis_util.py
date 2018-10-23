import requests
import json
import os
import logging

def get_headers():

    if 'HYPOTHESIS_TOKEN' in os.environ:
        token = os.environ['HYPOTHESIS_TOKEN']
    else:
        raise Exception("Need to specify Hypothesis token with HYPOTHESIS_TOKEN env var")
    
    auth_header = 'Bearer %s'%(token)

    return {'Authorization': auth_header}


def basic_auth():

    url = ' https://hypothes.is/api'

    # Get the authorization header
    headers = get_headers()

    # Make the request
    response = requests.get(url, headers=headers)

    if response.status_code==200:

        # Interpret results as JSON
        dat = response.json()

        msg = json.dumps(dat, indent=4)
        logging.info(msg)

    else:

        msg = "Response status code was not OK: %d"%(response.status_code)
        logging.info(msg)


def list_annotations():
    # kEaohJC9Eeiy_UOozkpkyA

    url = 'https://hypothes.is/api/annotations/kEaohJC9Eeiy_UOozkpkyA'

    # Get the authorization header
    headers = get_headers()

    # Make the request
    response = requests.get(url, headers=headers)

    if response.status_code==200:

        # Interpret results as JSON
        dat = response.json()

        msg = json.dumps(dat, indent=4)
        logging.info(msg)

    else:

        msg = "Response status code was not OK: %d"%(response.status_code)
        logging.info(msg)


def search_annotations():
    url = ' https://hypothes.is/api/search'

    # Get the authorization header
    headers = get_headers()

    # Set query params
    params = dict(
            url = '*pilot.nihdatacommons.us*',
            limit = 200
    )
    #http://pilot.nihdatacommons.us/organize/CopperInternalDeliveryWorkFlow/',

    # Make the request
    response = requests.get(url, headers=headers, params=params)

    if response.status_code==200:

        # Interpret results as JSON
        dat = response.json()

        msg = json.dumps(dat, indent=4)
        logging.info(msg)

    else:

        msg = "Response status code was not OK: %d"%(response.status_code)
        logging.info(msg)


if __name__=="__main__":
    search_annotations()

