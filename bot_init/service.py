import re
from time import sleep

from django.conf import settings
from telebot import TeleBot

from bot_init.models import Subscriber
from bot_init.schemas import Answer
from bot_init.markup import get_default_keyboard
from game.models import MembersGroup, PointsRecord


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
    return Answer("Добро пожаловать!", keyboard=get_default_keyboard())


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


def write_points(chat_id: int, points_count: int):
    subscriber = get_subscriber_by_chat_id(chat_id)
    PointsRecord.objects.create(subscriber=subscriber, points_count=points_count)


def get_subscriber_point_count(subscriber: Subscriber) -> int:
    points_records = PointsRecord.objects.filter(subscriber=subscriber)
    result = 0
    for elem in points_records:
        result += elem.points_count
    return result


def get_subscriber_statistic_by_chat_id(chat_id: int) -> int:
    subscriber = get_subscriber_by_chat_id(chat_id)
    return get_subscriber_point_count(subscriber)


def get_group_statistic_by_chat_id(chat_id: int) -> int:
    subscriber = get_subscriber_by_chat_id(chat_id)
    group = subscriber.members_group
    group_points = sum([get_subscriber_point_count(subscriber) for subscriber in group.subscribers.all()])
    return group_points


def text_message_service(chat_id: int, text: str):
    if text == '📈Статистика':
        subscriber_points = get_subscriber_statistic_by_chat_id(chat_id)
        group_points = get_group_statistic_by_chat_id(chat_id)
        text = f'Баллов у группы: {group_points}\nБаллов у вас: {subscriber_points}'
        return Answer(text, keyboard=get_default_keyboard())
    elif regexp_result := re.search(r'\d+', text):
        if not True: # TODO проверка по времени от 20 до 24 часов, единственная запись в день
            return
        write_points(chat_id, regexp_result.group(0))
        return Answer(f'Засчитано {text} очков')
