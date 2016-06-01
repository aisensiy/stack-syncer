import requests
import config
import logging

logger = logging.getLogger()


def login():
    session = requests.Session()
    r = session.post(config.KETSU_ENTRYPOINT + '/authentication',
                     json={'user_name': config.KETSU_USERNAME, 'user_password': config.KETSU_PASSWORD})
    if r.status_code != 200:
        logger.info("Fail to log in ketsu")
        raise "Fail to log in ketsu"
    return session
