## How does centillion use the Disqus API?

The Disqus API takes a URL and returns a comment thread.

Start with the [using the api](https://help.disqus.com/developer/using-the-api)
instructions at the disqus help site.

First step is to [create an api application](https://help.disqus.com/api/how-to-create-an-api-application).

From the private-www mkdocs.yml we know the name
of the comments forum that is embedded on the site:

```
dcppc-internal
```

Documentation for all endpoints is [here](https://disqus.com/api/docs/).

Below is a simple example of how we can list all threads in a forum:

```
$ curl -0 -L "https://disqus.com/api/3.0/threads/list.json?forum=dcppc-internal&api_key=<insert-public-api-key-here>
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 22009  100 22009    0     0  41625      0 --:--:-- --:--:-- --:--:-- 41604
{
    "cursor": {
        "prev": null,
        "hasNext": true,
        "next": "1534004357707360:0:0",
        "hasPrev": false,
        "total": null,
        "id": "1534004357707360:0:0",
        "more": true
    },
    "code": 0,
    "response": [
        {
            "feed": "https://dcppc-internal.disqus.com/readme_data_commons_internal_site_98/latest.rss",
            "author": "26946287",
            "dislikes": 0,
            "likes": 0,
            "message": "",
            "isSpam": false,
            "isDeleted": false,
            "category": "7717589",
            "clean_title": "README - Data Commons Internal Site",
            "userScore": 0,
            "id": "6866453106",
            "signedLink": "http://disq.us/?url=http%3A%2F%2Fpilot.data-commons.us%2Forganize%2Fproject-management%2F&key=T-kr-H0Ll82g9pVYgBgoXA",
            "createdAt": "2018-08-21T17:07:54",
            "hasStreaming": false,
            "raw_message": "",
            "isClosed": false,
            "link": "http://pilot.data-commons.us/organize/project-management/",
            "slug": "readme_data_commons_internal_site_98",
            "forum": "dcppc-internal",
            "identifiers": [
                "/organize/project-management/"
            ],
            "posts": 0,
            "userSubscription": false,
            "validateAllPosts": false,
            "title": "README - Data Commons Internal Site",
            "highlightedPost": null
        },

        ...

        {
            "editableUntil": "2018-08-28T21:56:00",
            "dislikes": 0,
            "numReports": 0,
            "likes": 0,
            "message": "<p>This is a second test comment!</p>",
            "id": "4052680814",
            "createdAt": "2018-08-21T21:56:00",
            "author": {
                "username": "disqus_OUz8lgSWvL",
                "about": "",
                "name": "charles reid",
                "disable3rdPartyTrackers": false,
                "isPowerContributor": false,
                "joinedAt": "2018-08-10T00:45:42",
                "profileUrl": "https://disqus.com/by/disqus_OUz8lgSWvL/",
                "url": "",
                "location": "",
                "isPrivate": false,
                "signedUrl": "",
                "isPrimary": true,
                "isAnonymous": false,
                "id": "294244984",
                "avatar": {
                    "small": {
                        "permalink": "https://disqus.com/api/users/avatars/disqus_OUz8lgSWvL.jpg",
                        "cache": "https://c.disquscdn.com/uploads/users/29424/4984/avatar32.jpg?1534888632"
                    },
                    "isCustom": true,
                    "permalink": "https://disqus.com/api/users/avatars/disqus_OUz8lgSWvL.jpg",
                    "cache": "https://c.disquscdn.com/uploads/users/29424/4984/avatar92.jpg?1534888632",
                    "large": {
                        "permalink": "https://disqus.com/api/users/avatars/disqus_OUz8lgSWvL.jpg",
                        "cache": "https://c.disquscdn.com/uploads/users/29424/4984/avatar92.jpg?1534888632"
                    }
                }
            },
            "media": [],
            "isSpam": false,
            "isDeletedByAuthor": false,
            "isDeleted": false,
            "parent": null,
            "isApproved": true,
            "isFlagged": false,
            "raw_message": "This is a second test comment!",
            "isHighlighted": false,
            "canVote": false,
            "thread": "6845448591",
            "forum": "dcppc-internal",
            "points": 0,
            "moderationLabels": [],
            "isEdited": false,
            "sb": false
        }
    ]
}

```

