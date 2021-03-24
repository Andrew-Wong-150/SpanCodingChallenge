# SpanCodingChallenge

This reposity contains the code to implement Span's Backend Engineering Intern Take Home 2021 Coding Challenge

## Setup

```bash
git clone https://github.com/Andrew-Wong-150/SpanCodingChallenge
```

## Prerequisites
This program was developed on Python 3.8.5 without any additional 3rd party libraries.

## Usage

The file ```notifications.py``` contains three functions to modify Span app notifications. Their name and function are as followed:

- ```legacy_notification_port(notifications)``` -Coverts all old notifications to new notification format.


- ```deduplication(notifications)``` - Removes duplicate notifications in the new format, keeing the higher priority one. If two notifications share the same deduplication_id as well as priority, keep the later
    timestamp.

- ```sort_notifications(notifications)``` -Sorts notifications in the new format by timestamp(ascending) and then by priority(descending)

All functions require a ```notifications``` parameter which have the following structure:

For ```legacy_notification_port(notifications)```
```
[
   {
      "datestring": ISO 8601-formatted timestamp,
      "priority": "LOW" | "MID" | "HIGH",
      "msg": "{{title}}: {{body}}",
      "deduplication_id": string
   }
]
```

For other functions
```
[
   {
      "timestamp": unix timestamp (epoch) in milliseconds
      "priority": integer (2 is high, 1 is mid, 0 is low)
      "body": string,
      "title": string,
      "deduplication_id": string
   }
]
```

## Testing
To run the unit tests:
```bash
python test_notifications.py
```

## Author
Andrew Wong