from django.core.management.base import BaseCommand

from game.service import ask_about_task


class Command(BaseCommand):
    help = 'command for update webhook'

    def handle(self, *args, **options):
        ask_about_task()
