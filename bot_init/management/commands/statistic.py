from django.core.management.base import BaseCommand

from game.services.statistic import make_statistic


class Command(BaseCommand):
    help = 'command for update webhook'

    def handle(self, *args, **options):
        make_statistic(358610865)
