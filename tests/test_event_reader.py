import unittest
import json
from mockito import mock, when

from .context import syncer

data_for_empty_event_response = json.loads("""
{
  "next": "",
  "last": "http://controller.aisensiy.com/stack_events?per-page=10&page=1",
  "prev": "",
  "count": 0,
  "self": "http://controller.aisensiy.com/stack_events?per-page=10&page=1",
  "items": [],
  "first": "http://controller.aisensiy.com/stack_events?per-page=10&page=1"
}
""")

data_for_one_page_nonempty_event_response = json.loads("""
{
  "next": "",
  "last": "http://controller.aisensiy.com/stack_events?per-page=10&page=1",
  "prev": "",
  "count": 0,
  "self": "http://controller.aisensiy.com/stack_events?per-page=10&page=1",
  "items": [
      {
          "id": "a3aaa4edadbf4e5f86321c32b6628aef",
          "type": "StackUpdatedEvent",
          "content": {
            "createdAt": 1464769905000,
            "stack": {
              "name": "flask",
              "description": "A flask stack",
              "links": [
                {
                  "rel": "self",
                  "uri": "http://controller.aisensiy.com/stacks/a6159a6295b14a448567861d87cd834d"
                }
              ],
              "id": "a6159a6295b14a448567861d87cd834d",
              "status": "UNPUBLISHED"
            }
          }
        }
  ],
  "first": "http://controller.aisensiy.com/stack_events?per-page=10&page=1"
}
""")

data_for_nonempty_event_response = json.loads("""
{
  "next": "",
  "last": "http://controller.aisensiy.com/stack_events?per-page=10&page=1",
  "prev": "http://prev",
  "count": 0,
  "self": "http://controller.aisensiy.com/stack_events?per-page=10&page=1",
  "items": [
      {
          "id": "a3aaa4edadbf4e5f86321c32b6628aef",
          "type": "StackUpdatedEvent",
          "content": {
            "createdAt": 1464769905000,
            "stack": {
              "name": "flask",
              "description": "A flask stack",
              "links": [
                {
                  "rel": "self",
                  "uri": "http://controller.aisensiy.com/stacks/a6159a6295b14a448567861d87cd834d"
                }
              ],
              "id": "a6159a6295b14a448567861d87cd834d",
              "status": "UNPUBLISHED"
            }
          }
        }
  ],
  "first": "http://controller.aisensiy.com/stack_events?per-page=10&page=1"
}
""")


class TestEventReader(unittest.TestCase):

    def test_get_empty_list_if_no_events(self):
        mock_client = mock()
        when(mock_client).get('http://test').thenReturn((200, data_for_empty_event_response))
        reader = syncer.event_reader.EventReader(mock_client)
        result = reader.read_events('http://test', '')
        self.assertEqual(result, [])

    def test_get_non_empty_list(self):
        mock_client = mock()
        when(mock_client).get('http://test').thenReturn((200, data_for_one_page_nonempty_event_response))
        reader = syncer.event_reader.EventReader(mock_client)
        result = reader.read_events('http://test', '')
        self.assertEqual(len(result), 1)

    def test_get_empty_list_if_has_lastest_event_id(self):
        mock_client = mock()
        when(mock_client).get('http://test').thenReturn((200, data_for_one_page_nonempty_event_response))
        reader = syncer.event_reader.EventReader(mock_client)
        result = reader.read_events('http://test', 'a3aaa4edadbf4e5f86321c32b6628aef')
        self.assertEqual(len(result), 0)

    def test_should_read_previous_page_if_has(self):
        mock_client = mock()
        when(mock_client).get('http://test').thenReturn((200, data_for_nonempty_event_response))
        when(mock_client).get('http://prev').thenReturn((200, data_for_one_page_nonempty_event_response))
        reader = syncer.event_reader.EventReader(mock_client)
        result = reader.read_events('http://test', '')
        self.assertEqual(len(result), 2)