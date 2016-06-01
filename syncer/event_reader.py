import config
import logging
import processor
import sys
import os
from http_client import HttpClient

logger = logging.getLogger("event_reader")
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def read_events(url, last_event):
    status_code, data = HttpClient().get(url)
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
        return unprocessed_events + read_events(data['prev'], last_event, unprocessed_events)
    else:
        return unprocessed_events[::-1]
