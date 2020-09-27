from __future__ import absolute_import, unicode_literals
from celery.task import periodic_task
from celery.schedules import crontab

from game.service import send_daily_tasks


@periodic_task(run_every=(crontab(hour=7, minute=0)), name='mailing')
def mailing():
    send_daily_tasks()