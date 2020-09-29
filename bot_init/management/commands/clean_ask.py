from django.core.management.base import BaseCommand

from game.service import clean_ask


class Command(BaseCommand):
    help = 'command for update webhook'

    def handle(self, *args, **options):
        clean_ask()
