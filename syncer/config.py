import os

LAST_EVENT_FILE = os.getenv('STORAGE', '/data/last_event')
CDE_EVENT_ENTRYPOINT = os.getenv('CDE_EVENT_ENTRYPOINT', 'http://controller.aisensiy.com/stack_events')
KETSU_ENTRYPOINT = os.getenv('KETSU_ENTRYPOINT', 'http://ketsu-backend.aisensiy.com')
KETSU_USERNAME = os.getenv('KETSU_USERNAME', 'admin')
KETSU_PASSWORD = os.getenv('KETSU_PASSWORD', '123')