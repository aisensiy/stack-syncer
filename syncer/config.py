import os

CDE_EVENT_ENTRYPOINT = os.getenv('CDE_EVENT_ENTRYPOINT', 'http://controller.aisensiy.com/stack_events')
KETSU_ENTRYPOINT = os.getenv('KETSU_ENTRYPOINT', 'http://localhost:8088')
KETSU_USERNAME = os.getenv('KETSU_USERNAME', 'admin')
KETSU_PASSWORD = os.getenv('KETSU_PASSWORD', '123')