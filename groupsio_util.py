from bs4 import BeautifulSoup

class GroupsIOArchivesCrawler(object):
    """
    This is a Groups.io spider
    designed to crawl the email
    archives of a group.

    credentials (dictionary):
        groupsio_access_token :     api access token
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
        if self.crawled_archives:
            return self.archives
        else:
            self.crawl_group_archives()
            return self.archives


    def get_subgroups_list(self):
        """
        Use the API to get a list of subgroups.
        """
        subgroups_url = 'https://api.groups.io/v1/getsubgroups'

        key = self.credentials['groupsio_access_token']

        data = [('group_name', self.group_name),
                ('limit',100)
        ]
        response = requests.post(url,
                                 data=data,
                                 auth=(key,''))
        response = response.json()
        data = response['data']

        subgroups = {}
        for group in data:
            k = group['id']
            v = group['name']
            subgroups[k] = v

        return subgroups


    def crawl_group_archives(self):
        """
        Spider will crawl the email archives of the entire group
        by crawling the email archives of each subgroup.
        """
        subgroups = self.get_subgroups_list()

        # ------------------------------
        # Start by logging in.

        # Create session object to persist session data
        session = requests.Session()

        # Log in to the website
        data = dict(email = self.credentials['groupsio_username'],
                    password = self.credentials['groupsio_password'],
                    timezone = 'America/Los_Angeles')

        r = s.post(self.login_url,
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
        # self.archives is a list of dictionaries,
        # with each dictionary containing info about
        # a topic/email thread in a subgroup.
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

        """
        url = self.url.format(group=self.group_name, 
                              subgroup=subgroup_name)

        # ------------------------------

        s = session

        # Now get the first page
        r = s.get(url)

        # ------------------------------
        # Fencepost algorithm:

        # First page:

        # Extract a list of (title, link) items
        items = self.extract_archive_page_items_(r)

        for (title, link) in items:
            # Get the thread page:
            r = s.get(link)
            import pdb; pdb.set_trace()

            # Do processing:

            # what are we extracting:
            # 1. thread number
            # 2. permalink
            # 3. content/text (filtered)

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

            # 2.permalink:
            # - current link is ugly link
            # - permalink is the nice one
            # - topic id is available from the ugly link
            # https://{group}.groups.io/g/{subgroup}/topic/{topic_id}

            permalink_template = "https://{group}.groups.io/g/{subgroup}/topic/{topic_id}"
            permalink = permalink_template.format(
                    group = self.group_name,
                    subgroup = subgroup, 
                    topic_id = topic_id
            )

            # 3. content/text:
            # - Use the nice link to get the content of the thread
            # - Content filtering
            # - Extracting relevant information
            # - Bundling everything into email thread item
            # - (schema?)




        # This is the first in a paginated list of pages.
        # 
        # Fencepost algorithm:
        # 
        # first page:
        # Extract a list of (title, link) items
        # For each (title,link) item,
        #    Do some processing:
        #        Visit the link and assemble a dictionary
        #        Content filtering
        #        Title, id, permalink, author, content, date created, date indexed
        #        Return ful email thread item
        #
        # remaining pages:
        # while requests.get(next button link) returns ok:
        #    Extract a list of (title, link) items
        #    For each (title,link) item,
        #       Do some processing:
        #           Visit the link and assemble a dictionary
        #           Content filtering
        #           Title, id, permalink, author, content, date created, date indexed
        #           Return ful email thread item
        #    Add email thread item to archives 



        print(r)



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

        results = []
        for row in rows:
            # We don't care about anything except title and ugly link
            subject = row.find('span',{'class':'subject'})
            title = subject.get_text()
            link = row.find('a')['href']
            results.append((title,link))

        return results



