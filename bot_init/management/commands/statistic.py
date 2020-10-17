from django.core.management.base import BaseCommand

from game.services.statistic import make_statistic_by_month, make_statistic_by_two_week


class Command(BaseCommand):
    help = 'command for update webhook'

    def handle(self, *args, **options):
        make_statistic_by_month(358610865)
        make_statistic_by_two_week(358610865)
