from flask import Flask
from flask_apscheduler import APScheduler


class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': '__main__:sync_stack',
            'trigger': 'interval',
            'seconds': 10
        }
    ]

    SCHEDULER_VIEWS_ENABLED = True
    SCHEDULER_TIMEZONE = 'UTC'


def sync_stack():
    print 'hello world'


app = Flask(__name__)
app.config.from_object(Config())


@app.route("/")
def hello():
    return "Hello, world!"


if __name__ == "__main__":
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.run(host='0.0.0.0')
