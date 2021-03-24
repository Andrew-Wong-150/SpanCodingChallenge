import unittest
import notifications

class TestNotifications(unittest.TestCase):

    def test_legacy_notification_port_datestring_priority_msg(self):

        data = [
            {
                'datestring': '1970-01-01T00:00:00.100Z',
                'priority': 'HIGH',
                'msg': 'test_title: test_body',
                'deduplication_id': 'test_id'
            }
        ]

        expected = [
            {
                'timestamp': 100,
                'priority': 2,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'test_id'
            }
        ]

        result = notifications.legacy_notification_port(data)
        self.assertEqual(result, expected)


    def test_legacy_notification_port_empty(self):

        data = []
        self.assertRaises(TypeError, notifications.legacy_notification_port, data)


    def test_legacy_notification_port_missing_keys(self):

        data = [
            {
               'datestring': '1970-01-01T00:00:00.100Z' 
            }
        ]
        self.assertRaises(KeyError, notifications.legacy_notification_port, data)


    def test_deduplication_empty(self):

        data = []
        self.assertRaises(TypeError, notifications.deduplication, data)


    def test_deduplication_keys(self):

        data = [
            {
               'timestamp': 100 
            }
        ]
        self.assertRaises(KeyError, notifications.deduplication, data)


    def test_deduplication_no_duplicates(self):

        data = [
            {
                'timestamp': 1,
                'priority': 0,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id1'
            },
            {
                'timestamp': 2,
                'priority': 1,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id2'
            },
            {
                'timestamp': 3,
                'priority': 2,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id3'
            }
        ]

        result = notifications.deduplication(data)
        self.assertCountEqual(result, data)


    def test_deduplication_same_id_different_priorities(self):

        data = [
            {
                'timestamp': 1,
                'priority': 0,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id1'
            },
            {
                'timestamp': 2,
                'priority': 1,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id1'
            },
            {
                'timestamp': 3,
                'priority': 2,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id1'
            }
        ]

        expected = [
            {
                'timestamp': 3,
                'priority': 2,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id1'
            }
        ]

        result = notifications.deduplication(data)
        self.assertEqual(result, expected)


    def test_deduplication_multi_same_id_different_priorities(self):

        data = [
            {
                'timestamp': 1,
                'priority': 1,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id1'
            },
            {
                'timestamp': 2,
                'priority': 2,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id1'
            },
            {
                'timestamp': 3,
                'priority': 2,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id2'
            },
                        {
                'timestamp': 4,
                'priority': 0,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id2'
            }
            
        ]

        expected = [
            {
                'timestamp': 2,
                'priority': 2,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id1'
            },
            {
                'timestamp': 3,
                'priority': 2,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id2'
            }
        ]

        result = notifications.deduplication(data)
        self.assertEqual(result, expected)


    def test_deduplication_same_id_same_priorities(self):

        data = [
            {
                'timestamp': 1,
                'priority': 1,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id1'
            },
            {
                'timestamp': 2,
                'priority': 1,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id1'
            },
            {
                'timestamp': 3,
                'priority': 1,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id1'
            }
        ]

        expected = [
            {
                'timestamp': 3,
                'priority': 1,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id1'
            }
        ]

        result = notifications.deduplication(data)
        self.assertEqual(result, expected)


    def test_deduplication_multi_same_id_same_priorities(self):

        data = [
            {
                'timestamp': 1,
                'priority': 1,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id1'
            },
            {
                'timestamp': 2,
                'priority': 1,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id1'
            },
            {
                'timestamp': 3,
                'priority': 1,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id2'
            },
                        {
                'timestamp': 4,
                'priority': 1,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id2'
            }
            
        ]

        expected = [
            {
                'timestamp': 2,
                'priority': 1,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id1'
            },
            {
                'timestamp': 4,
                'priority': 1,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id2'
            }
        ]

        result = notifications.deduplication(data)
        self.assertEqual(result, expected)


    def test_sort_notification_empty(self):

        data = []
        self.assertRaises(TypeError, notifications.sort_notification, data)


    def test_sort_notification_keys(self):

        data = [
            {
               'timestamp': 100 
            }
        ]
        self.assertRaises(KeyError, notifications.sort_notification, data)


    def test_sort_notification_pre_sorted(self):

        data = [
            {
                'timestamp': 1,
                'priority': 2,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id1'
            },
            {
                'timestamp': 2,
                'priority': 1,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id2'
            },
            {
                'timestamp': 3,
                'priority': 0,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id3'
            }
        ]

        result = notifications.sort_notification(data)
        self.assertEqual(result, data)


    def test_sort_notification_mixed_timestamp(self):

        data = [
            {
                'timestamp': 2,
                'priority': 2,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id2'
            },
            {
                'timestamp': 1,
                'priority': 1,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id1'
            },
            {
                'timestamp': 3,
                'priority': 0,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id3'
            }
        ]

        expected = [
            {
                'timestamp': 1,
                'priority': 1,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id1'
            },
            {
                'timestamp': 2,
                'priority': 2,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id2'
            },
            {
                'timestamp': 3,
                'priority': 0,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id3'
            }
        ]

        result = notifications.sort_notification(data)
        self.assertEqual(result, expected)


    def test_sort_notification_mixed_priorities(self):

        data = [
            {
                'timestamp': 1,
                'priority': 0,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id1'
            },
            {
                'timestamp': 2,
                'priority': 2,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id2'
            },
            {
                'timestamp': 3,
                'priority': 1,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id3'
            }
        ]

        expected = [
            {
                'timestamp': 1,
                'priority': 0,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id1'
            },
            {
                'timestamp': 2,
                'priority': 2,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id2'
            },
            {
                'timestamp': 3,
                'priority': 1,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id3'
            }
        ]

        result = notifications.sort_notification(data)
        self.assertEqual(result, expected)


    def test_sort_notification_mixed_timestamp_and_mixed_priorities(self):

        data = [
            {
                'timestamp': 2,
                'priority': 2,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id2'
            },
            {
                'timestamp': 1,
                'priority': 1,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id1'
            },
            {
                'timestamp': 3,
                'priority': 0,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id3'
            }
        ]

        expected = [
            {
                'timestamp': 1,
                'priority': 1,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id1'
            },
            {
                'timestamp': 2,
                'priority': 2,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id2'
            },
            {
                'timestamp': 3,
                'priority': 0,
                'body': 'test_body',
                'title': 'test_title',
                'deduplication_id': 'id3'
            }
        ]

        result = notifications.sort_notification(data)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()