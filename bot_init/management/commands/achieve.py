import json

from django.core.management.base import BaseCommand
from telebot.types import InputMediaPhoto

from game.models import DailyTask
from bot_init.utils import get_tbot_instance


class Command(BaseCommand):
    help = 'command for update webhook'

    def handle(self, *args, **options):
        tbot = get_tbot_instance()
        caption="Брат, ты с успехом прошёл этот месяц! Альхамдулиллах! Знаю, было тяжело, где-то лениво, но ты справился. Ты усердно выполнял задачи, которые ставил перед собой. И вот твой заслуженный подарок - наглядное доказательство того, что ты можешь всё! Продолжай свой путь воспитания Нафса и укрепления Имана. Алга, брат! Бисмиллях!"
        with open('tmp.json', 'r') as f:
            data = json.load(f)
        for key, value in data.items():
            images = []
            for elem in value:
                qs = DailyTask.objects.filter(text=elem, image__isnull=False)
                for x in qs:
                    if x.image and len(images) < 10:
                        images.append(InputMediaPhoto(x.image))
                    else:
                        ...
            try:
                tbot.send_media_group(key, images)
                tbot.send_message(key, text=caption)
            except Exception as e:
                print(e)
