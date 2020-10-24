from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import telebot
from loguru import logger

from config.settings import TG_BOT
from bot_init.service import registration_subscriber, text_message_service, handle_query_service
from bot_init.utils import save_message
from bot_init.schemas import Answer


log = logger.bind(task="write_in_data")
logger.add(f"{settings.BASE_DIR}/logs/in_data.log", filter=lambda record: record["extra"]["task"] == "write_in_data")

token = TG_BOT.token
tbot = telebot.TeleBot(TG_BOT.token)


@csrf_exempt
def bot(request):
    """Обработчик пакетов от телеграмма"""
    if request.content_type == 'application/json':
        json_data = request.body.decode('utf-8')
        log.info(json_data)
        update = telebot.types.Update.de_json(json_data)
        tbot.process_new_updates([update])
        return HttpResponse('')
    else:
        raise PermissionDenied


@tbot.message_handler(commands=['start'])
def start_handler(message):
    """Обработчик команды /start"""
    save_message(message)
    answer = registration_subscriber(message.chat.id, message.text)
    answer.send(chat_id=message.chat.id)


@tbot.message_handler(content_types=['text'])
def text_handler(message):
    save_message(message)
    answer = text_message_service(message.chat.id, message.text)
    if isinstance(answer, Answer):
        answer.send(chat_id=message.chat.id)


@tbot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    """Обравботка нажатий на инлайн кнопку"""
    answer = handle_query_service(
        chat_id=call.from_user.id,
        text=call.data,
        message_id=call.message.message_id,
        message_text=call.message.text,
        call_id=call.id
    )
    if isinstance(answer, Answer):
        answer.edit(call.message.message_id)
