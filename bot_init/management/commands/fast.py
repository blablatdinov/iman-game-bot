from django.core.management.base import BaseCommand

from game.service import send_daily_tasks


class Command(BaseCommand):
    help = 'command for update webhook'

    def handle(self, *args, **options):
        send_daily_tasks()
