import config
import logging
import sys
import os
from http_client import HttpClient
import event_reader

logger = logging.getLogger("processor")
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

http_client = HttpClient()


def login():
    url = config.KETSU_ENTRYPOINT + '/authentication'
    logging.info("POST %s", url)
    status_code = http_client.post(url,
                                   json={'user_name': config.KETSU_USERNAME, 'user_password': config.KETSU_PASSWORD})
    if status_code != 200:
        raise Exception("Fail to login ketsu")


def create_stack(event):
    login()
    stack = event['content']['stack']
    if stack is None or stack['id'] is None or stack['name'] is None:
        raise Exception('on stack created event no id or name')

    status_code = http_client.post(config.KETSU_ENTRYPOINT + '/stacks', json={'id': stack['id'], 'name': stack['name']})
    logger.info("import stack %s %s get %d", stack['id'], stack['name'], status_code)


def update_stack(event):
    login()
    stack = event['content']['stack']
    if stack is None or stack['id'] is None or stack['name'] is None:
        raise Exception('on stack updated event no id or name')

    status_code = http_client.put(config.KETSU_ENTRYPOINT + '/stacks/' + stack['id'], json={'name': stack['name']})
    logger.info("update stack %s %s get %d", stack['id'], stack['name'], status_code)


def load_last_event_id():
    if not os.path.isfile(config.LAST_EVENT_FILE):
        return ''
    return open(config.LAST_EVENT_FILE).read()


def save_last_event_id(last_event):
    with open(config.LAST_EVENT_FILE, 'w') as f:
        f.write(last_event)


def process():
    last_event_id = load_last_event_id()
    logger.info('last event %s', last_event_id)
    events = event_reader.read_events(config.CDE_EVENT_ENTRYPOINT, last_event_id)
    logger.info('events %d', len(events))
    for event in events:
        if event['type'] == 'StackCreatedEvent':
            create_stack(event)
        elif event['type'] == 'StackUpdatedEvent':
            update_stack(event)
    len(events) and save_last_event_id(events[-1]['id'])


if __name__ == '__main__':
    last_event = load_last_event_id()
    logger.info('last event %s', last_event)
    events = event_reader.read_events(config.CDE_EVENT_ENTRYPOINT, last_event)
    print events
