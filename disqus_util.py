import requests
import json

from pprint import pprint

"""
Convenience class wrapper for Disqus comments.

This requires that the user provide either their
API OAuth application credentials (in which case
a user needs to authenticate with the application
so it can access the comments that they can see)
or user credentials from a previous login.
"""


def list_threads():

    # list all threads
    list_threads_url = 'https://disqus.com/api/3.0/threads/list.json'

    # list all posts (comments)
    list_posts_url = 'https://disqus.com/api/3.0/threads/listPosts.json'

    base_params = dict(
            api_key='ooi9rHjmzRhFHtANfZ2I221L7BtHfRfHZPr9nerlfx4v2SAhi2PcWtBvoz7SU2FW',
            forum='dcppc-internal'
    )

    # prepare url params
    params = {}
    for k in base_params.keys():
        params[k] = base_params[k]

    # make api call (first loop in fencepost)
    results = requests.request('GET', list_threads_url, params=params).json()
    cursor = results['cursor']
    responses = results['response']

    threads = {}
    comments = {}

    while True:

        for response in responses:
            if '127.0.0.1' not in response['link'] and 'localhost' not in response['link']:

                # Save thread info
                thread_id = response['id']
                thread_count = response['posts']

                if thread_id=='6845448591':
                    import pdb; pdb.set_trace()
                    z=0
                print("Working on thread %s (%d posts)"%(thread_id,thread_count))
                if thread_count > 0:
                    threads[thread_id] = response

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
                            print("    + %s"%(comment['message']))
                            thread_comments.append(comment)
                   
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

                    comments[thread_id] = thread_comments


        if cursor['hasNext']:

            # Prepare for next URL call
            params = {}
            for k in base_params.keys():
                params[k] = base_params[k]
            params['cursor'] = cursor['next']

            # Make the next URL call
            results = requests.request('GET', list_threads_url, params=params).json()
            cursor = results['cursor']
            responses = results['response']

            print("\nNext Page\n")

        else:
            break


if __name__=="__main__":
    list_threads()

