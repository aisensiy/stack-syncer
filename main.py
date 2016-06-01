from flask import Flask
from flask_apscheduler import APScheduler
from syncer import event_reader


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
    event_reader.subscribe_events()


app = Flask(__name__)
app.config.from_object(Config())


@app.route("/")
def hello():
    return "Last sync id: " + event_reader.load_last_event_id()


if __name__ == "__main__":
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.run(host='0.0.0.0')
