from django.core.management.base import BaseCommand

from game.service import send_list_with_selected_tasks


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        send_list_with_selected_tasks()
