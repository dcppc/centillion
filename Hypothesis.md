# Hypothesis API


## Authenticating

Example output call for authenticating with the API:

```
{
    "links": {
        "profile": {
            "read": {
                "url": "https://hypothes.is/api/profile",
                "method": "GET",
                "desc": "Fetch the user's profile"
            },
            "update": {
                "url": "https://hypothes.is/api/profile",
                "method": "PATCH",
                "desc": "Update a user's preferences"
            }
        },
        "search": {
            "url": "https://hypothes.is/api/search",
            "method": "GET",
            "desc": "Search for annotations"
        },
        "group": {
            "member": {
                "add": {
                    "url": "https://hypothes.is/api/groups/:pubid/members/:userid",
                    "method": "POST",
                    "desc": "Add the user in the request params to a group."
                },
                "delete": {
                    "url": "https://hypothes.is/api/groups/:pubid/members/:userid",
                    "method": "DELETE",
                    "desc": "Remove the current user from a group."
                }
            }
        },
        "links": {
            "url": "https://hypothes.is/api/links",
            "method": "GET",
            "desc": "URL templates for generating URLs for HTML pages"
        },
        "groups": {
            "read": {
                "url": "https://hypothes.is/api/groups",
                "method": "GET",
                "desc": "Fetch the user's groups"
            }
        },
        "annotation": {
            "hide": {
                "url": "https://hypothes.is/api/annotations/:id/hide",
                "method": "PUT",
                "desc": "Hide an annotation as a group moderator."
            },
            "unhide": {
                "url": "https://hypothes.is/api/annotations/:id/hide",
                "method": "DELETE",
                "desc": "Unhide an annotation as a group moderator."
            },
            "read": {
                "url": "https://hypothes.is/api/annotations/:id",
                "method": "GET",
                "desc": "Fetch an annotation"
            },
            "create": {
                "url": "https://hypothes.is/api/annotations",
                "method": "POST",
                "desc": "Create an annotation"
            },
            "update": {
                "url": "https://hypothes.is/api/annotations/:id",
                "method": "PATCH",
                "desc": "Update an annotation"
            },
            "flag": {
                "url": "https://hypothes.is/api/annotations/:id/flag",
                "method": "PUT",
                "desc": "Flag an annotation for review."
            },
            "delete": {
                "url": "https://hypothes.is/api/annotations/:id",
                "method": "DELETE",
                "desc": "Delete an annotation"
            }
        }
    }
}
```


## Listing

Here is the result of the API call to list an annotation
given its annotation ID:

```
{
    "updated": "2018-07-26T10:20:47.803636+00:00",
    "group": "__world__",
    "target": [
        {
            "source": "https://h.readthedocs.io/en/latest/api/authorization/",
            "selector": [
                {
                    "conformsTo": "https://tools.ietf.org/html/rfc3236",
                    "type": "FragmentSelector",
                    "value": "access-tokens"
                },
                {
                    "endContainer": "/div[1]/section[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/p[2]",
                    "startContainer": "/div[1]/section[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/p[1]",
                    "type": "RangeSelector",
                    "startOffset": 14,
                    "endOffset": 116
                },
                {
                    "type": "TextPositionSelector",
                    "end": 2234,
                    "start": 1374
                },
                {
                    "exact": "hich read or write data as a specific user need to be authorized\nwith an access token. Access tokens can be obtained in two ways:\n\nBy generating a personal API token on the Hypothesis developer\npage (you must be logged in to\nHypothesis to get to this page). This is the simplest method, however\nthese tokens are only suitable for enabling your application to make\nrequests as a single specific user.\n\nBy registering an \u201cOAuth client\u201d and\nimplementing the OAuth authentication flow\nin your application. This method allows any user to authorize your\napplication to read and write data via the API as that user.  The Hypothesis\nclient is an example of an application that uses OAuth.\nSee Using OAuth for details of how to implement this method.\n\n\nOnce an access token has been obtained, requests can be authorized by putting\nthe token in the Authorization header.",
                    "prefix": "\n\n\nAccess tokens\u00b6\nAPI requests w",
                    "type": "TextQuoteSelector",
                    "suffix": "\nExample request:\nGET /api HTTP/"
                }
            ]
        }
    ],
    "links": {
        "json": "https://hypothes.is/api/annotations/kEaohJC9Eeiy_UOozkpkyA",
        "html": "https://hypothes.is/a/kEaohJC9Eeiy_UOozkpkyA",
        "incontext": "https://hyp.is/kEaohJC9Eeiy_UOozkpkyA/h.readthedocs.io/en/latest/api/authorization/"
    },
    "tags": [],
    "text": "sdfsdf",
    "created": "2018-07-26T10:20:47.803636+00:00",
    "uri": "https://h.readthedocs.io/en/latest/api/authorization/",
    "flagged": false,
    "user_info": {
        "display_name": null
    },
    "user": "acct:Aravindan@hypothes.is",
    "hidden": false,
    "document": {
        "title": [
            "Authorization \u2014 h 0.0.2 documentation"
        ]
    },
    "id": "kEaohJC9Eeiy_UOozkpkyA",
    "permissions": {
        "read": [
            "group:__world__"
        ],
        "admin": [
            "acct:Aravindan@hypothes.is"
        ],
        "update": [
            "acct:Aravindan@hypothes.is"
        ],
        "delete": [
            "acct:Aravindan@hypothes.is"
        ]
    }
}
```

