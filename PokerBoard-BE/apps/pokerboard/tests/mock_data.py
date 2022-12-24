COMMENTS_REPONSE = {
    "startAt": 0,
    "maxResults": 1048576,
    "total": 13,
    "comments": [
        {
            "author": {
                "displayName": "Rohit Jain",
            },
            "body": "Mera comment 2",
            "created": "2021-08-27T12:00:51.059+0530"
        },
        {
            "author": {
                "displayName": "Rohit Jain",
            },
            "body": "Mera comment 2",
            "created": "2021-08-27T12:33:14.663+0530"
        }
    ]
}

JQL_RESPONSE = {
    "expand": "schema,names",
    "startAt": 0,
    "maxResults": 50,
    "total": 2,
    "issues": [
        {
            "key": "KD-4",
            "fields": {
                "created": "2021-07-10T11:24:35.125+0530",
                "customfield_10016": 2.0,
                "summary": "Add subroute to display and edit an issue's details"
                
            }
        },
        {
            "key": "KD-3",
            "fields": {
                "created": "2021-07-10T11:24:35.125+0530",
                "customfield_10016": 2.0,
                "summary": "Add subroute to display and edit an issue's details"
                
            }
        },
    ]
}

BOARDS_RESPONSE = {
    "maxResults": 50,
    "startAt": 0,
    "total": 2,
    "values": [
        {
            "id": 2,
            "self": "https://kaam-dhandha.atlassian.net/rest/agile/1.0/board/2",
            "name": "BB board",
            "type": "scrum",
            "location": {
                "projectId": 10002,
                "displayName": "bugs board (BB)",
                "projectName": "bugs board",
                "projectKey": "BB",
                "projectTypeKey": "software",
                "avatarURI": "/secure/projectavatar?size=small&s=small&pid=10002&avatarId=10404",
                "name": "bugs board (BB)"
            }
        }
    ]
}

SPRINTS_RESPONSE = {
    "maxResults": 50,
    "startAt": 0,
    "isLast": True,
    "values": [
        {
            "id": 3,
            "self": "https://kaam-dhandha.atlassian.net/rest/agile/1.0/sprint/3",
            "state": "future",
            "name": "BB Sprint 1",
            "originBoardId": 2
        }
    ]
}
