from celery import Celery
import config
from slackbot import spam2slack


APP = Celery('tasx', broker=config.RABBIT_URL)


@APP.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    MEMEPOST_INTERVAL = 60 * 10
    sender.add_periodic_task(MEMEPOST_INTERVAL, beat_memes.s())


@APP.task()
def beat_memes():
    spam2slack()
