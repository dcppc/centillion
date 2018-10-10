import requests, os, io, re
import json
import logging

import dateutil.parser
import datetime

from zipfile import ZipFile, BadZipFile
from mailbox import mbox

from bs4 import BeautifulSoup

class GroupsIOException(Exception):
    pass


###############################
# Functions for extracting 
# email information from
# mailing list archives

def get_mbox_archives(groupsio_token,config):
    """
    Use the Groups.io API to obtain an mbox file
    for every subgroup. For each subgroup mbox file,
    parse it and add the email threads to a big
    final archive (dictionary).

    Returns the final archive.

    {
        <permalink> : {
                        'permalink': <permalink>,
                        'created_time': <date>,
                        'subject': <subject>,
                        'subgroup': <subgroup>
                        'sender_name': <name>,
                        'sender_email': <email>,
                        'content': <content>
                    }
    }
    """
    final_archive = {}

    subgroup_ids = get_all_subgroups(groupsio_token)

    for j, subgroup_id in enumerate(subgroup_ids.keys()):

        subgroup_name = subgroup_ids[subgroup_id]

        # This function call below will call
        # get_archive_zip for each subgroup,
        # and extract the mbox contents from
        # the zip file.
        html = extract_mbox_from_zip(subgroup_name, subgroup_id, groupsio_token)

        # Now extract each email thread and 
        # add to final_archive dictionary
        subgroup_archive = extract_threads_from_mbox(html, subgroup_name)

        # keys = permalinks
        # values = dictionary of thread info

        # Merge subgroup archive into final archive
        merge_dicts(
                merge_from = subgroup_archive,
                merge_into = final_archive
        )

        if config['TESTING'] is True and j>=1:
            break

    return final_archive


def merge_dicts(merge_from,merge_into):
    """
    Utility function to merge two dictionaries.
    Strategy: don't overwrite any values in merge_into.
    """
    for k in merge_from.keys():
        if k not in merge_into.keys():
            merge_into[k] = merge_from[k]


def extract_threads_from_mbox(mbox_file, subgroup_name):
    """
    Extract threads from an mbox file (HTML format).
    This comes after you've already downloaded the 
    zip file from the Groups.io API, extracted the
    HTML contents of the mbox file, and passed it 
    here (mbox_file).
    """
    subgroup_archive = {}

    # Clean up temporary mbox file
    tempf = '.delete_me'
    if os.path.exists(tempf):
        os.remove(tempf)

    # Dump temporary mbox file
    with open(tempf,'wb') as f:
        f.write(mbox_file)

    # Read temporary mbox file
    m = mbox(tempf)

    # Delete temporary mbox file
    os.remove(tempf)

    msgs = m.items()
    n_msgs = len(msgs)

    logging.info("=============================")
    logging.info("Processing mbox %s with %s messages"%(mbox_file,n_msgs))

    findall_email_pattern  = re.compile('.*<.*>')
    finditer_email_pattern = re.compile('"(.*)" <(.*)>')

    for i,msg in msgs:

        logging.info("Processing message %02d of %02d"%(i+1, n_msgs))

        #{
        #    <permalink> : {
        #                    'permalink': <permalink>,
        #                    'date': <date>,
        #                    'subject': <subject>,
        #                    '(sender)name': <name>,
        #                    '(sender)email': <email>,
        #                    'subgroup': <subgroup>
        #                    'content': <content>
        #                }
        #}

        short_subgroup_name = re.findall('\+(.*)$',subgroup_name)[0]

        permalink = "https://dcppc.groups.io/g/%s/message/%d"%(short_subgroup_name,i+1)

        archive_item = {}

        archive_item['permalink']   = permalink
        archive_item['date']        = msg['Date']
        archive_item['subject']     = msg['Subject']
        archive_item['subgroup']    = short_subgroup_name

        # process the from field
        try:
            if len(re.findall(findall_email_pattern,msg['From']))>0:
                # We have a From field in format
                # "Name" <email>
                for result in re.finditer(finditer_email_pattern,msg['From']):
                    (from_name, from_email) = result.groups()
                    archive_item['sender_name'] = from_name
                    archive_item['sender_email'] = from_email
            else:
                archive_item['sender_name'] = ''
                archive_item['sender_email'] = msg['From']
        except:
            raise Exception("Crashed on From extraction regular expressions")

        # process the email content
        if msg.is_multipart():
            for part in msg.walk():
                if part.is_multipart():
                    for subpart in part.walk():
                        if subpart.get_content_type() == 'text/plain':
                            body = subpart.get_payload(decode=True)
                elif part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True)
        elif msg.get_content_type() == 'text/plain':
            body = msg.get_payload(decode=True)

        archive_item['content'] = str(body)

        subgroup_archive[permalink] = archive_item

    return subgroup_archive


def extract_mbox_from_zip(subgroup_name, subgroup_id, groupsio_token):
    """
    Extract an mbox file from the zip file for this subgroup.
    The zip file stays in memory, and is not written to disk.
    """
    z = get_archive_zip(subgroup_name, subgroup_id, groupsio_token)
    if z is not None:
        file_contents = {name:z.read(name) for name in z.namelist()}
        html = file_contents['messages.mbox']
        os.remove('messages.mbox')
        return html


def get_all_subgroups(groupsio_token):
    """
    Returns a dictionary where keys are subgroup ids
    and values are subgroup names
    """
    MAX_GROUPS=100
    url = 'https://api.groups.io/v1/getsubgroups'

    key = groupsio_token

    data = [ ('group_name','dcppc'),
             ('limit',MAX_GROUPS)]

    response = requests.post(url,data=data,auth=(key,''))
    response = response.json()
    try:
        dat = response['data']
    except:
        print(response)
        raise Exception("Error getting subgroups")

    all_subgroups = {}
    for group in dat:
        all_subgroups[group['id']] = group['name']
    return all_subgroups


def get_archive_zip(group_name, group_id, groupsio_token): 
    """
    Use the API to extract a zipped .mbox email archive
    for one subgroup, and return the contents as z.
    """
    url = "https://api.groups.io/v1/downloadarchives"
    
    key = groupsio_token
    
    data = [('group_id',group_id)]

    print("get_archive_zip(): getting .mbox archive for subgroup %s (%s)"%(group_name,group_id))
    r = requests.post(url,data=data,auth=(key,''),stream=True)
    
    try:
        z = ZipFile(io.BytesIO(r.content))
        z.extractall()
        print("SUCCESS: subgroup %s worked"%(group_name))
        print("")
        return z
    except BadZipFile:
        print("ABORTING: subgroup %s failed"%(group_name))
        print(r.content.decode('utf-8'))
        print("")
        return None

