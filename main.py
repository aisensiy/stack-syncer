from flask import Flask
from flask_apscheduler import APScheduler
from syncer import processor, http_client, config, event_reader


class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': '__main__:sync_stack',
            'trigger': 'interval',
            'seconds': 60
        }
    ]

    SCHEDULER_VIEWS_ENABLED = True
    SCHEDULER_TIMEZONE = 'UTC'


def sync_stack():
    runner = processor.Processor(http_client.HttpClient(), config.LAST_EVENT_FILE)
    runner.process(event_reader.EventReader(http_client.HttpClient()))


app = Flask(__name__)
app.config.from_object(Config())


@app.route("/")
def hello():
    return "Last sync id: " + processor.load_last_event_id()


if __name__ == "__main__":
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.run(host='0.0.0.0')
