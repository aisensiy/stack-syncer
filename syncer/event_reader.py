import logging
import sys

logger = logging.getLogger("event_reader")
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class EventReader:
    def __init__(self, client):
        self.client = client

    def read_events(self, url, last_event):
        status_code, data = self.client.get(url)
        logger.info("get events %s", url)

        reach_latest = False

        unprocessed_events = []

        for event in data['items'][::-1]:
            print 'event id', event['id']
            print last_event
            if event['id'] == last_event:
                reach_latest = True
                break
            else:
                unprocessed_events.append(event)

        if not reach_latest and len(data['prev']):
            return unprocessed_events + self.read_events(data['prev'], last_event)
        else:
            return unprocessed_events[::-1]
