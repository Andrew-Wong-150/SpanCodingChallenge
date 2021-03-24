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
    '''
    Part 1: Legacy Notification Port. Coverts all old notifications to new notification format.
    
    Args:
        notifications: An array of old format notifications to be converted.

    Returns:
        List of notifications updated to new notification format
    
    Raises:
        TypeError: If the input is empty
        KeyError: If the input is missing notification keys
    '''

    # ensure input is not empty
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
    '''
    Part 2: De-duplicating. Removes duplicate notifications in the new format, keeing the higher priority one. If two
    notifications share the same deduplication_id as well as priority, keep the later timestamp.
    
    Args:
        notifications: An array of new format notifications to remove duplications from.
    
    Returns:
        List of selected notifications with the highest priority / latest timestamp
    
    Raises:
        TypeError: If the input is empty
        KeyError: If the input is missing notification keys
    '''

    # ensure input is not empty
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
    '''
    Part 3: Sorting. Sorts notifications in the new format by timestamp(ascending) and then by priority(descending)
    
    Args:
        notifications: An array of new format notifications to be sorted.
    
    Returns:
        List of notifications sorted by timestamp and priority

    Raises:
        TypeError: If the input is empty
        KeyError: If the input is missing notification keys
    '''

    # ensure input is not empty
    if not notifications:
        raise TypeError('Input is empty')

    # sort using timestamp and priority as sort key
    try:
        notifications = sorted(notifications, key=lambda x: [x['timestamp'], -x['priority']])
    except KeyError:
        raise KeyError('Notification data is missing keys')
    
    return notifications