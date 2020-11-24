import json
from pprint import pprint

from django.core.management.base import BaseCommand
from django.utils import timezone

from game.services.statistic import get_plus_per_period
from bot_init.models import Subscriber
from game.models import DailyTask


class Command(BaseCommand):
    help = 'command for update webhook'

    def handle(self, *args, **options):
        res = dict()
        res2 = dict()
        for sub in Subscriber.objects.filter(is_active=True):
            for task in DailyTask.objects.all():
                if sub.daily_tasks_records.filter(task__text=task.text, is_done=True).count() > 3:
                    if not sub.tg_chat_id in res:
                        res[sub.tg_chat_id] = [task.text]
                    else:
                        res[sub.tg_chat_id] += [task.text]
        for key, value in res.items():
            res2[key] = list(set(res[key]))
        with open('tmp.json', 'w') as f:
            json.dump(res2, f, ensure_ascii=False, indent=2)
        for key, value in res2.items():
            print(key)
            for elem in value:
                print(f" - {elem}")
                    #print(sub, task.text)
