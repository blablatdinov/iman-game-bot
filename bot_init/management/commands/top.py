from django.core.management.base import BaseCommand
from django.utils import timezone

from game.services.statistic import get_plus_per_period
from bot_init.models import Subscriber


class Command(BaseCommand):
    help = 'command for update webhook'

    def handle(self, *args, **options):
        for s in Subscriber.objects.filter(is_active=True):
            period = (
                s.registry_date,
                timezone.now().date()
            )
            try:
                pluses = get_plus_per_period(s, period)
                print(s, sum(pluses) / 10)
            except Exception as e:
                print(e)
