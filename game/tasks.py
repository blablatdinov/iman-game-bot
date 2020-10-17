from __future__ import absolute_import, unicode_literals
from celery.task import periodic_task
from celery.schedules import crontab

from game.service import send_daily_tasks, ask_about_task, clean_ask, send_reminders, clean_ques


@periodic_task(run_every=(crontab(hour=7, minute=0)), name='send_daily_tasks')
def celery_send_daily_tasks():
    send_daily_tasks()


@periodic_task(run_every=(crontab(hour=21, minute=0)), name='ask_about_task')
def celery_ask_about_task():
    ask_about_task()


@periodic_task(run_every=(crontab(hour=0, minute=0)), name='clean_asks')
def celery_clean_ask():
    clean_ask()


@periodic_task(run_every=(crontab(hour=16, minute=0)), name='send_reminders')
def send_reminders_task():
    send_reminders()


@periodic_task(run_every=(crontab(hour=9, minute=0)), name='clean_ques')
def clean_ques_task():
    clean_ques()
