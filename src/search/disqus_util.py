import os, re
import requests
import json
import dateutil.parser
import logging

from pprint import pprint

"""
Convenience class wrapper for Disqus comments.

This requires that the user provide either their
API OAuth application credentials (in which case
a user needs to authenticate with the application
so it can access the comments that they can see)
or user credentials from a previous login.
"""

class DisqusCrawler(object):

    def __init__(self,
                 credentials,
                 group_name):

        self.credentials = credentials
        self.group_name = group_name
        self.crawled_comments = False
        self.threads = None


    def get_threads(self):
        """
        Return a list of dictionaries containing
        entries for each comment thread in the given 
        disqus forum.
        """
        return self.threads


    def crawl_threads(self):
        """
        This will use the API to get every thread,
        and will iterate through every thread to 
        get every comment thread. 
        """
        # The money shot
        threads = {}

        # list all threads
        list_threads_url = 'https://disqus.com/api/3.0/threads/list.json'

        # list all posts (comments)
        list_posts_url = 'https://disqus.com/api/3.0/threads/listPosts.json'

        base_params = dict(
                api_key=self.credentials,
                forum=self.group_name
        )

        # prepare url params
        params = {}
        for k in base_params.keys():
            params[k] = base_params[k]

        # make api call (first loop in fencepost)
        results = requests.request('GET', list_threads_url, params=params).json()
        cursor = results['cursor']
        responses = results['response']

        while True:

            for response in responses:
                if '127.0.0.1' not in response['link'] and 'localhost' not in response['link']:

                    # Save thread info
                    thread_id = response['id']
                    thread_count = response['posts']

                    msg = "Working on thread %s (%d posts)"%(thread_id,thread_count)
                    logging.info(msg)

                    if thread_count > 0:

                        # prepare url params
                        params_comments = {}
                        for k in base_params.keys():
                            params_comments[k] = base_params[k]

                        params_comments['thread'] = thread_id

                        # make api call
                        results_comments = requests.request('GET', list_posts_url, params=params_comments).json()
                        cursor_comments = results_comments['cursor']
                        responses_comments = results_comments['response']

                        # Save comments for this thread
                        thread_comments = []

                        while True:
                            for comment in responses_comments:
                                # Save comment info
                                msg = "    + %s"%(comment['message'])
                                logging.info(msg)

                                thread_comments.append(comment['message'])
                       
                            if cursor_comments['hasNext']:
                       
                                # Prepare for the next URL call
                                params_comments = {}
                                for k in base_params.keys():
                                    params_comments[k] = base_params[k]
                                params_comments['thread'] = thread_id
                                params_comments['cursor'] = cursor_comments['next']
                       
                                # Make the next URL call
                                results_comments = requests.request('GET', list_posts_url, params=params_comments).json()
                                cursor_comments = results_comments['cursor']
                                responses_comments = results_comments['response']
                       
                            else:
                               break

                        link = response['link']
                        clean_link = re.sub('data-commons.us','nihdatacommons.us',link)
                        clean_link += "#disqus_comments"

                        # Finished working on thread.

                        # We need to make this value a dictionary
                        thread_info = dict(
                                id = response['id'],
                                created_time = dateutil.parser.parse(response['createdAt']),
                                title = response['title'],
                                forum = response['forum'],
                                link = clean_link,
                                content = "\n\n-----".join(thread_comments)
                        )
                        threads[thread_id] = thread_info


            if 'hasNext' in cursor.keys() and cursor['hasNext']:

                # Prepare for next URL call
                params = {}
                for k in base_params.keys():
                    params[k] = base_params[k]
                params['cursor'] = cursor['next']

                # Make the next URL call
                results = requests.request('GET', list_threads_url, params=params).json()
                cursor = results['cursor']
                responses = results['response']

            else:
                break

        self.threads = threads

