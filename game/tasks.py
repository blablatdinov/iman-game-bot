from __future__ import absolute_import, unicode_literals

from datetime import timedelta, date

from celery.task import periodic_task
from celery.schedules import crontab

from bot_init.models import Subscriber
from game.service import send_daily_tasks, ask_about_task, clean_ask, send_reminders, clean_ques
from game.services.statistic import make_statistic_by_month, make_statistic_by_two_week


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


@periodic_task(run_every=(crontab(hour=14, minute=0)), name='check_statistic_time')
def check_statistic_time_task():
    for subscriber in Subscriber.objects.filter(is_active=True):
        if subscriber.registry_date + timedelta(days=30) == date.today():
            make_statistic_by_month(subscriber.tg_chat_id)
        elif subscriber.registry_date + timedelta(days=14) == date.today():
            make_statistic_by_two_week(subscriber.tg_chat_id)
