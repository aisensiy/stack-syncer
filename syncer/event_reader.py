import config
import logging
import processor
import sys
import os
from http_client import HttpClient

logger = logging.getLogger()
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def read_events(url, last_event, events=[]):
    status_code, data = HttpClient().get(url)
    logger.info("get events %s", url)

    is_latest = False

    for event in data['items'][::-1]:
        if event['id'] == last_event:
            is_latest = True
            break
        else:
            events.append(event)

    if not is_latest and len(data['prev']):
        return read_events(data['prev'], last_event, events)
    else:
        return events[::-1]
