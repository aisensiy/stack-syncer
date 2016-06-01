import requests
import config
import logging
import sys

logger = logging.getLogger()
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def login():
    session = requests.Session()
    url = config.KETSU_ENTRYPOINT + '/authentication'
    logging.info("POST %s", url)
    r = session.post(url,
                     json={'user_name': config.KETSU_USERNAME, 'user_password': config.KETSU_PASSWORD})
    if r.status_code != 200:
        logger.info("Fail to log in ketsu")
        raise Exception("Fail to log in ketsu")
    return session


def on_stack_created(event):
    session = login()
    stack = event['content']['stack']
    if stack is None or stack['id'] is None or stack['name'] is None:
        raise Exception('on stack created event no id or name')

    response = session.post(config.KETSU_ENTRYPOINT + '/stacks', json={'id': stack['id'], 'name': stack['name']})
    logger.info("import stack %s %s get %d", stack['id'], stack['name'], response.status_code)


def on_stack_updated(event):
    session = login()
    stack = event['content']['stack']
    if stack is None or stack['id'] is None or stack['name'] is None:
        raise Exception('on stack updated event no id or name')

    response = session.put(config.KETSU_ENTRYPOINT + '/stacks/' + stack['id'], json={'name': stack['name']})
    logger.info("update stack %s %s get %d", stack['id'], stack['name'], response.status_code)
