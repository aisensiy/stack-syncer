import config
import logging
import event_handler
import requests
import sys
import os

logger = logging.getLogger()
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def load_last_event_id():
    if not os.path.isfile(config.LAST_EVENT_FILE):
        return ''
    return open(config.LAST_EVENT_FILE).read()


def save_last_event_id(last_event):
    with open(config.LAST_EVENT_FILE, 'w') as f:
        f.write(last_event)


def read_events(url, last_event, events=[]):
    response = requests.get(url)
    logger.info("get events %s", url)
    data = response.json()

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


def parse_events(events):
    for event in events:
        if event['type'] == 'StackCreatedEvent':
            event_handler.on_stack_created(event)
        elif event['type'] == 'StackUpdatedEvent':
            event_handler.on_stack_updated(event)


def subscribe_events():
    last_event_id = load_last_event_id()
    logger.info('last event %s', last_event_id)
    events = read_events(config.CDE_EVENT_ENTRYPOINT, last_event_id)
    parse_events(events)
    len(events) and save_last_event_id(events[-1]['id'])


if __name__ == '__main__':
    last_event_id = load_last_event_id()
    logger.info('last event %s', last_event_id)
    events = read_events(config.CDE_EVENT_ENTRYPOINT, last_event_id)
    print events
