import config
import logging
import sys
import os
from http_client import HttpClient

logger = logging.getLogger("processor")
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

http_client = HttpClient()


class Processor:
    def __init__(self, client, storage_path):
        self.client = client
        self.storage_path = storage_path

    def _login(self):
        url = config.KETSU_ENTRYPOINT + '/authentication'
        logging.info("POST %s", url)
        status_code = http_client.post(url,
                                       json={'user_name': config.KETSU_USERNAME,
                                             'user_password': config.KETSU_PASSWORD})
        if status_code != 200:
            logger.info("Fail to login ketsu")
            return False
        return True

    def _create_stack(self, event):
        if not self._login():
            return
        stack = event['content']['stack']
        if stack is None or 'id' not in stack or stack['id'] is None or 'name' not in stack or stack['name'] is None:
            logger.info("on stack created event no id or name")
            return

        status_code = http_client.post(config.KETSU_ENTRYPOINT + '/stacks',
                                       json={'id': stack['id'], 'name': stack['name']})
        logger.info("import stack %s %s get %d", stack['id'], stack['name'], status_code)

    def _update_stack(self, event):
        if not self._login():
            return
        stack = event['content']['stack']
        if stack is None or 'id' not in stack or stack['id'] is None or 'name' not in stack or stack['name'] is None:
            logger.info("on stack update event no id or name")
            return

        status_code = http_client.put(config.KETSU_ENTRYPOINT + '/stacks/' + stack['id'], json={'name': stack['name']})
        logger.info("update stack %s %s get %d", stack['id'], stack['name'], status_code)

    def load_last_event_id(self):
        if not os.path.isfile(config.LAST_EVENT_FILE):
            return ''
        return open(self.storage_path).read()

    def save_last_event_id(self, last_event):
        with open(self.storage_path, 'w') as f:
            f.write(last_event)

    def process(self, event_reader):
        last_event_id = self.load_last_event_id()
        logger.info('last event %s', last_event_id)
        events = event_reader.read_events(config.CDE_EVENT_ENTRYPOINT, last_event_id)
        logger.info('events %d', len(events))
        for event in events:
            if event['type'] == 'StackCreatedEvent':
                self._create_stack(event)
            elif event['type'] == 'StackUpdatedEvent':
                self._update_stack(event)
        len(events) and self.save_last_event_id(events[-1]['id'])
