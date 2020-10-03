import re
import pytz
import datetime
from time import sleep

from django.conf import settings
from django.utils import timezone
from telebot import TeleBot
from loguru import logger

from bot_init.models import Subscriber
from bot_init.schemas import Answer
from bot_init.markup import get_default_keyboard
from game.models import MembersGroup, PointsRecord, RecordDailyTask, RecordDailyTaskGroup
from game.service import translate_tasks_in_keyboard, get_text, ask_single_task
from game.services.survey import get_next_question


logger.add(f"{settings.BASE_DIR}/logs/app.log")


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


def allow_time_for_write_points():
    now = timezone.now()
    print(f'{now.hour + 3=}')
    return 20 <= now.hour + 3 <= 24


def check_points_count_for_today(chat_id):
    subscriber = get_subscriber_by_chat_id(chat_id)
    now = timezone.now()
    today_date = datetime.datetime(now.year, now.month, now.day)
    tomorrow_date = datetime.datetime(now.year, now.month, now.day + 1)
    points_records = PointsRecord.objects.filter(
        subscriber=subscriber,
        date__range=(today_date, tomorrow_date)
    )
    return points_records.count()

def text_message_service(chat_id: int, text: str):
    if text == '📈Статистика':
        subscriber_points = get_subscriber_statistic_by_chat_id(chat_id)
        group_points = get_group_statistic_by_chat_id(chat_id)
        text = f'Баллов у группы: {group_points}\nБаллов у вас: {subscriber_points}'
        return Answer(text, keyboard=get_default_keyboard())
    elif regexp_result := re.search(r'\d+', text):
        if not allow_time_for_write_points() and check_points_count_for_today(chat_id): # TODO проверка по времени от 20 до 24 часов, единственная запись в день
            return Answer(f'Очки можно присылать с 20 до 24 часов')
        write_points(chat_id, regexp_result.group(0))
        return Answer(f'Засчитано {text} очков')


def ask_about_today_points():
    answer = Answer('Введите сколько очков вы набрали сегодня')
    for subscriber in Subscriber.objects.filter(is_active=True):
        answer.send(subscriber.tg_chat_id)


def handle_query_service(chat_id: int, text: str, message_id: int, message_text: str, call_id: int):
    logger.info(f"{chat_id=} {text}")
    if "set_to_selected" in text:
        record_daily_task_id = int(re.search(r'\d+', text).group(0))
        record_daily_task = RecordDailyTask.objects.get(pk=record_daily_task_id)
        record_daily_task.switch()
        record_daily_task_group = record_daily_task.group
        tasks = record_daily_task_group.daily_tasks_records.all()
        keyboard = translate_tasks_in_keyboard(tasks)
        text = get_text([x.task for x in record_daily_task_group.daily_tasks_records.all()])
        return Answer(text, keyboard=keyboard, chat_id=chat_id)
    elif "set_to_done" in text:
        task_id, task_status, next_tasks_list = eval(re.search(r'\(.+\)', text).group(0))
        if task_status:
            task = RecordDailyTask.objects.get(pk=task_id)
            task.set_done()
        if len(next_tasks_list) == 0:
            tg_delete_message(chat_id=chat_id, message_id=message_id)
            Answer('Отлично, отчет готов', keyboard=get_default_keyboard(), chat_id=chat_id).send()
            return
        text, keyboard = ask_single_task(next_tasks_list)
        return Answer(text, keyboard=keyboard, chat_id=chat_id)
    elif "begin_survey" in text:
        value, begin_question_pk = eval(re.search(r'\(.+\)', text).group(0))
        answer = get_next_question(begin_question_pk)
        answer.chat_id = chat_id
        return answer


def tg_delete_message(chat_id, message_id):
    get_tbot_instance().delete_message(chat_id=chat_id, message_id=message_id)