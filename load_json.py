import notifications
import json
import sys

def parse_file(file_name):
    '''
    Loads Json file to port, deduplicate, and sort using the functions in notifications.py
    
    Args:
        file_name: Name of json file to load.
    '''

    # load json data from file
    with open(file_name) as fp:
        data = json.load(fp)

    # port, deduplicate, and sort data
    ported_data = notifications.legacy_notification_port(data)
    deduped_data = notifications.deduplication(ported_data)
    sorted_data = notifications.sort_notification(deduped_data)

    # write data to output file
    with open('output.json', 'w') as fp:
        json.dump(sorted_data, fp, indent=4)


if __name__ == '__main__':
    file_name = sys.argv[1]
    parse_file(file_name)