from time import sleep

from django.conf import settings
from telebot import TeleBot

from bot_init.models import Subscriber
from bot_init.schemas import Answer
from game.models import MembersGroup


def get_primary_key_from_start_message(text: str) -> int:
    return int(text[7:])


def registration_subscriber(chat_id: int, text: str):
    """Логика сохранения подписчика"""
    try:
        pk = get_primary_key_from_start_message(text)
        members_group = MembersGroup.objects.get(pk=pk)
    except ValueError:
        return Answer("Получите ссылку-приглашение для вашей команды")
    subscriber, created = Subscriber.objects.get_or_create(tg_chat_id=chat_id, members_group=members_group)
    return Answer("Добро пожаловать!")


def get_tbot_instance():
    return TeleBot(settings.TG_BOT.token)


def update_webhook(host=f'{settings.TG_BOT.webhook_host}/{settings.TG_BOT.token}'):
    """Обновляем webhook"""
    tbot = get_tbot_instance()
    tbot.remove_webhook()
    sleep(1)
    web = tbot.set_webhook(host)


def get_subscriber_by_chat_id(chat_id: int):
    try:
        subscriber = Subscriber.objects.get(tg_chat_id=chat_id)
        return subscriber
    except Subscriber.DoesNotExist:
        pass  # TODO что будем делать в этом случае


def text_message_service(chat_id: int, text: str):
    if True:
        subscriber = get_subscriber_by_chat_id(chat_id)
        group = subscriber.members_group
        group_points = sum([subscriber.points for subscriber in group.subscribers.all()])
        text = f'Баллов у группы: {group_points}\nБаллов у вас: {subscriber.points}'
        return Answer(text)
