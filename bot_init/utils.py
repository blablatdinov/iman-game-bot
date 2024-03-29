import json
from datetime import datetime

from django.utils.timezone import make_aware
from django.conf import settings
from telebot import TeleBot
from loguru import logger

from bot_init.models import Message, Subscriber

log = logger.bind(task="app")


def save_message(msg, message_key=None):
    """ Сохранение сообщения от пользователя """
    date = make_aware(datetime.fromtimestamp(msg.date))
    from_user_id = msg.from_user.id
    message_id = msg.message_id
    chat_id = msg.chat.id
    text = msg.text
    try:
        json_str = msg.json
    except:
        json_str = str(msg)
    json_text = json.dumps(json_str, indent=2, ensure_ascii=False)
    message_instance = Message.objects.create(
        date=date, from_user_id=from_user_id, message_id=message_id,
        chat_id=chat_id, text=text, json=json_text, key=message_key
    )
    return message_instance


def get_tbot_instance() -> TeleBot:
    """Получить объект для взаимодействия с api телеграма"""
    return TeleBot(settings.TG_BOT.token)


def tg_delete_message(chat_id, message_id):
    """Удалить сообщение в телеграм"""
    get_tbot_instance().delete_message(chat_id=chat_id, message_id=message_id)
    log.info(f"delete message (id: {message_id}, chat_id: {chat_id}")


def get_subscriber_by_chat_id(chat_id: int):
    """Получить подписчика по идентификатору чата"""
    try:
        subscriber = Subscriber.objects.get(tg_chat_id=chat_id)
        return subscriber
    except Subscriber.DoesNotExist:
        pass  # TODO что будем делать в этом случае


