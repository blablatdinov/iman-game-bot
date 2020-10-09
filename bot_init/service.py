import re
import datetime
from time import sleep

from django.conf import settings
from django.utils import timezone
from telebot import TeleBot
from loguru import logger

from bot_init.models import Subscriber, AdminMessage
from bot_init.schemas import Answer
from bot_init.markup import get_default_keyboard, InlineKeyboard
from game.models import MembersGroup, PointsRecord, RecordDailyTask, RecordDailyTaskGroup
from game.service import translate_tasks_in_keyboard, get_text, ask_single_task
from game.services.survey import get_next_question, set_points, start_survey


logger.add(f"{settings.BASE_DIR}/logs/app.log")


def get_primary_key_from_start_message(text: str) -> int:
    return int(text[7:])


def get_acquaintance_next_keyboard(step_num):
    buttons = [
        (('Вперед', f'acquaintance({step_num})'),)
    ]
    return InlineKeyboard(buttons).keyboard


def registration_subscriber(chat_id: int, text: str):
    """Логика сохранения подписчика"""
    try:
        pk = get_primary_key_from_start_message(text)
        members_group = MembersGroup.objects.get(pk=pk)
    except ValueError:
        return Answer("Получите ссылку-приглашение для вашей команды")
    subscriber, created = Subscriber.objects.get_or_create(tg_chat_id=chat_id, members_group=members_group)
    text = AdminMessage.objects.get(key='start').text
    keyboard = get_acquaintance_next_keyboard(1)
    return Answer(text, keyboard=keyboard)


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
    elif Subscriber.objects.get(tg_chat_id=chat_id).step == "ask_sub_purpose":
        admin_message = AdminMessage.objects.get(pk=4)
        text = admin_message.text
        keyboard = get_acquaintance_next_keyboard(4)
        print('\n' * 3)
        return Answer(text, keyboard=keyboard, chat_id=chat_id)


def handle_query_service(chat_id: int, text: str, message_id: int, message_text: str, call_id: int):
    # TODO побить функцию
    logger.info(f"{chat_id=} {text}")
    if "set_to_selected" in text:
        record_daily_task_id, level = eval(re.search(r'\(.+\)', text).group(0))
        record_daily_task = RecordDailyTask.objects.get(pk=record_daily_task_id)
        record_task_group = record_daily_task.group
        task_type = record_daily_task.task.task_type
        record_daily_task.switch()
        record_daily_task.complexity = level
        record_daily_task.save()
        tasks = record_task_group.daily_tasks_records.filter(task__task_type=task_type)
        # TODO выхардкодить индексы
        text = f"{tasks[0].task.get_task_type_display()}\n\n" \
               f"1) {tasks[0].task.text}\n" \
               f"2) {tasks[1].task.text}\n" \
               f"3) {tasks[2].task.text}\n"
        return Answer(text, keyboard=translate_tasks_in_keyboard(tasks), chat_id=chat_id)
    elif "set_to_unselected" in text:
        record_daily_task_id, level = eval(re.search(r'\(.+\)', text).group(0))
        record_daily_task = RecordDailyTask.objects.get(pk=record_daily_task_id)
        record_task_group = record_daily_task.group
        task_type = record_daily_task.task.task_type
        record_daily_task.switch()
        record_daily_task.complexity = 0
        record_daily_task.save()
        tasks = record_task_group.daily_tasks_records.filter(task__task_type=task_type)
        text = f"{tasks[0].task.get_task_type_display()}\n\n" \
               f"1) {tasks[0].task.text}\n" \
               f"2) {tasks[1].task.text}\n" \
               f"3) {tasks[2].task.text}\n"
        return Answer(text, keyboard=translate_tasks_in_keyboard(tasks), chat_id=chat_id)
    elif "set_to_done" in text:
        task_id, task_status, next_tasks_list = eval(re.search(r'\(.+\)', text).group(0))
        if task_status:
            task = RecordDailyTask.objects.get(pk=task_id)
            task.set_done()
        if len(next_tasks_list) == 0:
            if (subscriber := Subscriber.objects.get(tg_chat_id=chat_id).day) == 1:
                text = "Ну что, по основным моментам мы с тобой прошлись. " \
                       "Если остались вопросы, то задавай их в нашем Telegam чате или на " \
                       "странице в Инстаграм @iman.club\nНа этом все, ты выполняй задания, " \
                       "я буду их анализировать и через месяц покажу на сколько ты прибавил " \
                       "в каждом пункте своего развития. Алга, брат! Бисмиллях! "
                subscriber.day = 2
                subscriber.save()
            else:
                text = "Отлично, отчет готов"
            tg_delete_message(chat_id=chat_id, message_id=message_id)
            Answer(text, keyboard=get_default_keyboard(), chat_id=chat_id).send()
            return
        text, keyboard = ask_single_task(next_tasks_list)
        return Answer(text, keyboard=keyboard, chat_id=chat_id)
    elif "begin_survey" in text:
        value, begin_question_pk = eval(re.search(r'\(.+\)', text).group(0))
        set_points(chat_id, begin_question_pk, value)
        if begin_question_pk == 30:
            admin_message = AdminMessage.objects.get(pk=3)
            text = admin_message.text
            keyboard = get_acquaintance_next_keyboard(3)
            sub = Subscriber.objects.get(tg_chat_id=chat_id)
            sub.step = "ask_sub_purpose"
            sub.save()
            return Answer(text, keyboard=keyboard, chat_id=chat_id)
        answer = get_next_question(begin_question_pk)
        answer.chat_id = chat_id
        return answer
    elif "acquaintance" in text:
        step_num = int(re.search(r'\d+', text).group(0))
        if step_num == 5:
            admin_message = AdminMessage.objects.get(pk=step_num+1)
            Answer(admin_message.text, keyboard=get_default_keyboard(), chat_id=chat_id).send()
            return 
        elif step_num == 2:
            answer = start_survey(chat_id)
            return answer
        admin_message = AdminMessage.objects.get(pk=step_num+1)
        text = admin_message.text
        keyboard = get_acquaintance_next_keyboard(step_num + 1)
        Answer(text, keyboard=keyboard, chat_id=chat_id).send()
    elif "get_task_keyboard" in text:
        task_type, group_pk = eval(re.search(r'\(.+\)', text).group(0))
        task_group = RecordDailyTaskGroup.objects.get(pk=group_pk)
        tasks = [
            x for x in
            task_group.daily_tasks_records.filter(task__task_type=task_type)
        ]
        text = f"{tasks[0].task.get_task_type_display()}\n\n" \
               f"1) {tasks[0].task.text}\n" \
               f"2) {tasks[1].task.text}\n" \
               f"3) {tasks[2].task.text}\n"
        answer = Answer(text, keyboard=translate_tasks_in_keyboard(tasks), chat_id=chat_id)
        return answer


def tg_delete_message(chat_id, message_id):
    get_tbot_instance().delete_message(chat_id=chat_id, message_id=message_id)