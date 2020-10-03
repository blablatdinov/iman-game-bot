from django.core.management.base import BaseCommand

from game.services.survey import start_survey


class Command(BaseCommand):
    help = 'command for update webhook'

    def handle(self, *args, **options):
        start_survey()
