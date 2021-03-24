from enum import Enum
from datetime import datetime
from operator import itemgetter
import json

SECONDS_TO_MILLISECONDS = 1000
class Priority(Enum):
    HIGH = 2
    MID = 1
    LOW = 0


import json
from enum import Enum
from datetime import datetime
from operator import itemgetter

# define constant for time conversion
SECONDS_TO_MILLISECONDS = 1000

# create class to convert priority
class Priority(Enum):
    HIGH = 2
    MID = 1
    LOW = 0


def legacy_notification_port(notifications):

    if not notifications:
        raise TypeError('Input is empty')

    for item in notifications:
        
        try:
            # replace datestring with timestamp
            utc = datetime.strptime(item['datestring'], '%Y-%m-%dT%H:%M:%S.%fZ')
            epoch = int((utc - datetime(1970, 1, 1)).total_seconds() * SECONDS_TO_MILLISECONDS)
            
            item['timestamp'] = epoch
            del item['datestring']

            # update priority with numeric value
            item['priority'] = Priority[item['priority']].value

            # replace msg with title and body
            item['title'] = item['msg'].split(': ')[0]
            item['body'] = item['msg'].split(': ')[1]
            del item['msg']

        except KeyError:
            raise KeyError('Notification data is missing keys')

    return notifications


def deduplication(notifications):

    if not notifications:
        raise TypeError('Input is empty')

    selected_notifications = []

    for item in notifications:

        try:
            # only perform selection method for a new deduplication_id
            if not any(x['deduplication_id'] == item['deduplication_id'] for x in selected_notifications):

                # find all duplicate ids for current notifications
                duplicates = [x for x in notifications if x['deduplication_id'] == item['deduplication_id']]
                
                # find max priority of duplicates and remove all duplicates which do not have that priority
                max_priority = max([x['priority'] for x in duplicates])
                duplicates = [x for x in duplicates if x['priority'] == max_priority]

                # find latest timestamp of duplicates and remove all duplicates which do not have that timestamp
                latest_timestamp = max([x['timestamp'] for x in duplicates])
                duplicates = [x for x in duplicates if x['timestamp'] == latest_timestamp]

                # add selected notifications to list of notification to be sent to the user
                selected_notifications += duplicates
        
        except KeyError:
            raise KeyError('Notification data is missing keys')

    return selected_notifications


def sort_notification(notifications):

    if not notifications:
        raise TypeError('Input is empty')

    # sort using timestamp and priority as sort key
    try:
        notifications = sorted(notifications, key=lambda x: [x['timestamp'], -x['priority']])
    except KeyError:
        raise KeyError('Notification data is missing keys')
    
    return notifications


old_data = [
  {
    "datestring": "2021-03-20T00:37:48.100Z",
    "priority": "HIGH",
    "msg": "Title 1: Body 1",
    "deduplication_id": "id1"
  },
  {
    "datestring": "2021-03-19T00:29:04.375Z",
    "priority": "LOW",
    "msg": "Title 2: Body 2",
    "deduplication_id": "id2"
  },
]

new_data = [
  {
    "timestamp": 1,
    "priority": 0,
    "body": "Lorem ipsum",
    "title": "Title",
    "deduplication_id": "id1"
  },
  {
    "timestamp": 2,
    "priority": 1,
    "body": "Lorem ipsum",
    "title": "Title",
    "deduplication_id": "id1"
  },
  {
    "timestamp": 4,
    "priority": 0,
    "body": "Lorem ipsum",
    "title": "Title",
    "deduplication_id": "id2"
  },
  {
    "timestamp": 6,
    "priority": 1,
    "body": "Lorem ipsum",
    "title": "Title",
    "deduplication_id": "id2"
  },
  {
    "timestamp": 5,
    "priority": 2,
    "body": "Lorem ipsum",
    "title": "Title",
    "deduplication_id": "id2"
  }
]

result = deduplication(new_data)

print(json.dumps(result, indent=4, sort_keys=True))
