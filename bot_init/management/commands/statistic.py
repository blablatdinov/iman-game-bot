from django.core.management.base import BaseCommand

from bot_init.models import Subscriber
from game.services.statistic import make_statistic_by_month, make_statistic_by_two_week


class Command(BaseCommand):
    help = 'command for update webhook'

    def handle(self, *args, **options):
        for sub in Subscriber.objects.filter(is_active=True):
            #make_statistic_by_month(sub.tg_chat_id)
            make_statistic_by_two_week(sub.tg_chat_id)
