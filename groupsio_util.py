import requests, os, re
from bs4 import BeautifulSoup
import dateutil.parser
import datetime

class GroupsIOException(Exception):
    pass


###############################
# Functions for extracting 
# email information from
# mailing list archives
#
# 

def get_mbox_archives(groupsio_token):
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

    subgroup_ids = get_all_subgroups()
    for subgroup_id in subgroup_ids.keys():

        subgroup_name = subgroup_ids[subgroup_id]

        # This function call below will call
        # get_archive_zip for each subgroup,
        # and extract the mbox contents from
        # the zip file.
        html = extract_mbox_from_zip(subgroup_name, subgroup_id)

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

    m = mbox(mbox_file)
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

        archive_item = {}

        archive_item['permalink']   = permalink
        archive_item['date']        = msg['Date']
        archive_item['subject']     = msg['Subject']
        archive_item['subgroup']    = subgroup_name

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

        archive_item['content'] = body

        subgroup_archive[permalink] = archive_item

    return subgroup_archive


def extract_mbox_from_zip(subgroup_name, subgroup_id):
    """
    Extract an mbox file from the zip file for this subgroup
    """
    z = get_archive_zip(subgroup_name, subgroup_id)
    if z is not None:
        file_contents = {name:z.read(name) for name in z.namelist()}
        html = file_contents['messages.mbox']
        return html


def get_all_subgroups():
    """
    Returns a dictionary where keys are subgroup ids
    and values are subgroup names
    """
    MAX_GROUPS=100
    url = 'https://api.groups.io/v1/getsubgroups'

    try:
        key = os.environ['GROUPSIO_SECRET_TOKEN']
    except KeyError:
        err = "ERROR: You must set the GROUPSIO_SECRET_TOKEN environment variable. See README.md"
        raise Exception(err)

    data = [ ('group_name','dcppc'),
             ('limit',MAX_GROUPS)]

    response = requests.post(url,data=data,auth=(key,''))
    response = response.json()
    dat = response['data']

    all_subgroups = {}
    for group in dat:
        all_subgroups[group['id']] = group['name']
    return all_subgroups


def get_archive_zip(group_name,group_id): 
    """
    Use the API to extract a zipped .mbox email archive
    for one subgroup, and return the contents as z.
    """
    url = "https://api.groups.io/v1/downloadarchives"
    
    try:
        key = os.environ['GROUPSIO_SECRET_TOKEN']
    except KeyError:
        err = "ERROR: You must set the GROUPSIO_SECRET_TOKEN environment variable. See README.md"
        raise Exception(err)
    
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






# --------------------------------------------------
#
#             yuck
#
# --------------------------------------------------




class GroupsIOArchivesCrawler(object):
    """
    This is a Groups.io spider
    designed to crawl the email
    archives of a group.

    credentials (dictionary):
        groupsio_token :     api access token
        groupsio_username     :     username
        groupsio_password     :     password
    """
    def __init__(self,
                 credentials,
                 group_name):
        # template url for archives page (list of topics)
        self.url = "https://{group}.groups.io/g/{subgroup}/topics"
        self.login_url = "https://groups.io/login"

        self.credentials = credentials
        self.group_name = group_name
        self.crawled_archives = False
        self.archives = None


    def get_archives(self):
        """
        Return a list of dictionaries containing 
        information about each email topic in the 
        groups.io email archive.

        Call crawl_group_archives() first!
        """
        return self.archives


    def get_subgroups_list(self):
        """
        Use the API to get a list of subgroups.
        """
        subgroups_url = 'https://api.groups.io/v1/getsubgroups'

        key = self.credentials['groupsio_token']

        data = [('group_name', self.group_name),
                ('limit',100)
        ]
        response = requests.post(subgroups_url,
                                 data=data,
                                 auth=(key,''))
        response = response.json()

        # Check for errors
        if 'object' in response.keys():
            if response['object']=='error':
                err = "ERROR: groupsio_util.py: get_subgroups_list(): "
                err += "Problem calling the API, returned error:\n"
                err += str(response)
                raise Exception(err)

        # Check for data
        if 'data' in response.keys():
            data = response['data']
        else:
            err = "ERROR: groupsio_util.py: get_subgroups_list(): "
            err += "No 'data' key found in JSON response from API:\n"
            err += str(response)
            raise Exception(err)

        subgroups = {}
        for group in data:
            k = group['id']
            v = re.sub(r'dcppc\+','',group['name'])
            subgroups[k] = v

            ## Short circuit
            ## for debugging purposes
            #break

        return subgroups


    def crawl_group_archives(self):
        """
        Spider will crawl the email archives of the entire group
        by crawling the email archives of each subgroup.
        """
        self.archives = {}

        subgroups = self.get_subgroups_list()

        # ------------------------------
        # Start by logging in.

        # Create session object to persist session data
        session = requests.Session()

        # Log in to the website
        data = dict(email = self.credentials['groupsio_username'],
                    password = self.credentials['groupsio_password'],
                    timezone = 'America/Los_Angeles')

        r = session.post(self.login_url,
                         data = data)

        csrf = self.get_csrf(r)

        # ------------------------------
        # For each subgroup, crawl the archives
        # and return a list of dictionaries
        # containing all the email threads.
        for subgroup_id in subgroups.keys():
            self.crawl_subgroup_archives(session,
                                         csrf,
                                         subgroup_id, 
                                         subgroups[subgroup_id])

        # Done. archives are now tucked away
        # in the variable self.archives
        # 
        # self.archives is a dictionary of dictionaries,
        # with each key a URL and each value a dictionary
        # containing info about a thread.
        # ------------------------------




    def crawl_subgroup_archives(self, session, csrf, subgroup_id, subgroup_name):
        """
        This kicks off the process to crawl the entire
        archives of a given subgroup on groups.io.

        For a given subgroup the url is self.url,
        
            https://{group}.groups.io/g/{subgroup}/topics

        This is the first of a paginated list of topics.
        Procedure is:
        - passed a starting page (or its contents)
        - iterate through all topics via the HTML page elements
        - assemble a bundle of information about each topic:
            - topic title, by, URL, date, content, permalink
            - content filtering:
                - ^From, Reply-To, Date, To, Subject
                - Lines containing phone numbers
                    - 9 digits
                    - XXX-XXX-XXXX, (XXX) XXX-XXXX
                    - XXXXXXXXXX, XXX XXX XXXX
                    - ^Work: or (Work) or Work$
                    - Home, Cell, Mobile
                    - +1 XXX 
                    - \w@\w
        - while next button is not greyed out,
        - click the next button

        everything stored in self.archives:
        list of dictionaries.

        """
        prefix = "https://{group}.groups.io".format(group=self.group_name)

        url = self.url.format(group=self.group_name, 
                              subgroup=subgroup_name)

        # ------------------------------

        # Now get the first page
        r = session.get(url)

        # ------------------------------
        # Fencepost algorithm:

        # First page:

        # Extract a list of (title, link) items
        items = self.extract_archive_page_items_(r)

        # Get the next link
        next_url = self.get_next_url_(r)

        # Now add each item to the archive of threads,
        # then find the next button.
        self.add_items_to_archives_(session,subgroup_name,items)

        if next_url is None:
            return
        else:
            full_next_url = prefix + next_url

        # Now click the next button
        next_request = requests.get(full_next_url)

        while next_request.status_code==200:
            items = self.extract_archive_page_items_(next_request)
            next_url = self.get_next_url_(next_request)
            self.add_items_to_archives_(session,subgroup_name,items)
            if next_url is None:
                return
            else:
                full_next_url = prefix + next_url
            next_request = requests.get(full_next_url)
        


    def add_items_to_archives_(self,session,subgroup_name,items):
        """
        Given a set of items from a list of threads,
        items being title and link,
        get the page and store all info
        in self.archives variable
        (list of dictionaries)
        """
        for (title, link) in items:
            # Get the thread page:
            prefix = "https://{group}.groups.io".format(group=self.group_name)
            full_link = prefix + link
            r = session.get(full_link)
            soup = BeautifulSoup(r.text,'html.parser')

            # soup contains the entire thread

            # What are we extracting:
            # 1. thread number
            # 2. permalink
            # 3. content/text (filtered)

            # - - - - - - - - - - - - - - 
            # 1. topic/thread number:
            # <a rel="nofollow" href="">
            # where link is:
            # https://{group}.groups.io/g/{subgroup}/topic/{topic_id}
            # example topic id: 24209140
            #
            # ugly links are in the form 
            # https://dcppc.groups.io/g/{subgroup}/topic/some_text_here/{thread_id}?p=,,,,,1,2,3,,,4,,5
            # split at ?, 0th portion
            # then split at /, last (-1th) portion
            topic_id = link.split('?')[0].split('/')[-1]

            # - - - - - - - - - - - - - - - 
            # 2. permalink:
            # - current link is ugly link
            # - permalink is the nice one
            # - topic id is available from the ugly link
            # https://{group}.groups.io/g/{subgroup}/topic/{topic_id}

            permalink_template = "https://{group}.groups.io/g/{subgroup}/topic/{topic_id}"
            permalink = permalink_template.format(
                    group = self.group_name,
                    subgroup = subgroup_name, 
                    topic_id = topic_id
            )

            # - - - - - - - - - - - - - - - 
            # 3. content:

            # Need to rearrange how we're assembling threads here.
            # This is one thread, no?
            content = []

            subject = soup.find('title').text

            # Extract information for the schema:
            # - permalink for thread (done above)
            # - subject/title (done)
            # - original sender email/name (done)
            # - content (done)

            # Groups.io pages have zero CSS classes, which makes everything
            # a giant pain in the neck to interact with. Thanks Groups.io!
            original_sender = ''
            for i, tr in enumerate(soup.find_all('tr',{'class':'test'})):
                # Every other tr row contains an email.
                if (i+1)%2==0:
                    # nope, no email here
                    pass
                else:
                    # found an email!
                    # this is a maze, not amazing.
                    # thanks groups.io!
                    td = tr.find('td')

                    sender_divrow = td.find('div',{'class':'row'})
                    sender_divrow = sender_divrow.find('div',{'class':'pull-left'})
                    if (i+1)==1:
                        original_sender = sender_divrow.text.strip()

                    date_divrow = td.find('div',{'class':'row'})
                    date_divrow = date_divrow.find('div',{'class':'pull-right'})
                    date_divrow = date_divrow.find('font',{'class':'text-muted'})
                    date_divrow = date_divrow.find('script').text
                    try:
                        time_seconds = re.search(' [0-9]{1,} ',date_divrow).group(0)
                        time_seconds = time_seconds.strip()
                        # Thanks groups.io for the weird date formatting
                        time_seconds = time_seconds[:10]
                        mmicro_seconds = time_seconds[10:]
                        if (i+1)==1:
                            created_time  = datetime.datetime.utcfromtimestamp(int(time_seconds))
                            modified_time = datetime.datetime.utcfromtimestamp(int(time_seconds))
                        else:
                            modified_time = datetime.datetime.utcfromtimestamp(int(time_seconds))

                    except AttributeError:
                        created_time = None
                        modified_time = None

                    for div in td.find_all('div'):
                        if div.has_attr('id'):

                            # purge any signatures
                            for x in div.find_all('div',{'id':'Signature'}):
                                x.extract()

                            # purge any headers
                            for x in div.find_all('div'): 
                                nonos = ['From:','Sent:','To:','Cc:','CC:','Subject:']
                                for nono in nonos:
                                    if nono in x.text:
                                        x.extract()

                            message_text = div.get_text()

                            # More filtering:

                            # phone numbers
                            message_text = re.sub(r'[0-9]{3}-[0-9]{3}-[0-9]{4}','XXX-XXX-XXXX',message_text)
                            message_text = re.sub(r'[0-9]\{10\}','XXXXXXXXXX',message_text)

                            content.append(message_text)

            full_content = "\n".join(content)

            thread = {
                    'permalink' : permalink,
                    'created_time' : created_time,
                    'modified_time' : modified_time,
                    'subject' : subject,
                    'subgroup' : subgroup_name,
                    'original_sender' : original_sender,
                    'content' : full_content
            }

            print(" + Archiving thread: %s"%(thread['subject']))
            self.archives[permalink] = thread


    def extract_archive_page_items_(self, response):
        """
        (Private method)

        Given a response from a GET request,
        use beautifulsoup to extract all items
        (thread titles and ugly thread links)
        and pass them back in a list.
        """
        soup = BeautifulSoup(response.content,"html.parser")
        rows = soup.find_all('tr',{'class':'test'})
        if 'rate limited' in soup.text:
            raise GroupsIOException("Error: rate limit in place for Groups.io")

        results = []
        for row in rows:
            # This is where we extract
            # a list of thread titles 
            # and corresponding links.
            subject = row.find('span',{'class':'subject'})
            title = subject.get_text()
            link = row.find('a')['href']

            results.append((title,link))

        return results


    def get_next_url_(self, response):
        """
        (Private method)

        Given a response (which is a list of threads),
        find the next button and return the URL.

        If no next URL, if is disabled, then return None.
        """
        soup = BeautifulSoup(response.text,'html.parser')
        chevron = soup.find('i',{'class':'fa-chevron-right'})
        try:
            if '#' in chevron.parent['href']:
                # empty link, abort
                return None
        except AttributeError:
            # I don't even now
            return None

        if chevron.parent.parent.has_attr('class') and 'disabled' in chevron.parent.parent['class']:
            # no next link, abort
            return None

        return chevron.parent['href']



    def get_csrf(self,resp):
        """
        Find the CSRF token embedded in the subgroup page
        """
        soup = BeautifulSoup(resp.text,'html.parser')
        csrf = ''
        for i in soup.find_all('input'):
            # Note that i.name is different from i['name']
            # the first is the actual tag,
            # the second is the attribute name="xyz"
            if i['name']=='csrf':
                csrf = i['value']
        
        if csrf=='':
            err = "ERROR: Could not find csrf token on page."
            raise GroupsIOException(err)
    
        return csrf


