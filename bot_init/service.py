import re
from time import sleep

from django.conf import settings
from loguru import logger

from bot_init.models import Subscriber, AdminMessage
from bot_init.schemas import Answer
from bot_init.services.handle_service import set_task_to_selected_or_unselected, set_task_to_done, begin_survey, \
    acquaintance, get_task_keyboard
from bot_init.utils import get_tbot_instance
from bot_init.markup import InlineKeyboard
from game.models import MembersGroup

log = logger.bind(task="app")


def get_primary_key_from_start_message(text: str) -> int:
    """Достать идентификатор группы участников из стартового сообщения"""
    return int(text[7:])


def get_acquaintance_next_keyboard(step_num):  # TODO add type hints
    """Получить клавиатуру инструктажа"""
    buttons = [
        (('Вперед', f'acquaintance({step_num})'),)
    ]
    return InlineKeyboard(buttons).keyboard


def registration_subscriber(chat_id: int, text: str) -> Answer:
    """Логика сохранения подписчика"""
    try:
        pk = get_primary_key_from_start_message(text)
        members_group = MembersGroup.objects.get(pk=pk)
    except ValueError:
        return Answer("Получите ссылку-приглашение для вашей команды")
    subscriber, created = Subscriber.objects.get_or_create(tg_chat_id=chat_id, members_group=members_group)
    if created:
        text = AdminMessage.objects.get(key='start').text
        keyboard = get_acquaintance_next_keyboard(1)
        return Answer(text, keyboard=keyboard)
    return Answer("Вы уже зарегистрированы")


def update_webhook(host: str = f'{settings.TG_BOT.webhook_host}/{settings.TG_BOT.token}'):
    """Обновляем webhook"""
    tbot = get_tbot_instance()
    tbot.remove_webhook()
    sleep(1)
    web = tbot.set_webhook(host)
    return web


def text_message_service(chat_id: int, text: str):
    """Обработка текстовых сообщений"""
    if text == '📈Статистика':
        ...
    elif Subscriber.objects.get(tg_chat_id=chat_id).step == "ask_sub_purpose":
        admin_message = AdminMessage.objects.get(pk=4)
        text = admin_message.text
        keyboard = get_acquaintance_next_keyboard(4)
        return Answer(text, keyboard=keyboard, chat_id=chat_id)


def get_args(text):
    return eval(re.search(r'\(.+\)', text).group(0))


def handle_query_service(chat_id: int, text: str, message_id: int, message_text: str, call_id: int):
    """Обработка нажатий на inline кнопку"""
    log.info(f"{chat_id=} {text}")
    if "set_to_selected" in text or "set_to_unselected" in text:
        record_daily_task_id, level = get_args(text)
        answer = set_task_to_selected_or_unselected(record_daily_task_id, level, chat_id)
        return answer
    elif "set_to_done" in text or "settodone" in text:
        task_id, task_status, next_tasks_list = get_args(text)
        answer = set_task_to_done(
            task_id, task_status, next_tasks_list, chat_id, message_id
        )
        return answer
    elif "begin_survey" in text:
        value, begin_question_pk = get_args(text)
        answer = begin_survey(value, begin_question_pk, chat_id)
        return answer
    elif "acquaintance" in text:
        step_num = int(get_args(text))
        acquaintance(chat_id, step_num)
    elif "get_task_keyboard" in text:
        task_type, group_pk = get_args(text)
        get_task_keyboard(chat_id, task_type, group_pk)


