from random import choice

from django.utils import timezone

from bot_init.models import Subscriber
from bot_init.markup import InlineKeyboard
from bot_init.schemas import Answer
from game.schemas import DAILY_TASK_TYPE
from game.models import DailyTask, RecordDailyTask, RecordDailyTaskGroup


TASKS_TYPES = tuple([x[0] for x in DAILY_TASK_TYPE])


def get_tasks(day: int):
    """Функция возвращает список заданий для пользователя"""
    tasks = []
    for task_type in TASKS_TYPES:
        offset = day * 3  # TODO продумать механизм остатка, т. к. заданий ограниченное кол-во
        queryset = DailyTask.objects.filter(task_type=task_type).order_by("pk")
        queryset = queryset[offset:offset + 3]
        tasks += list(queryset)
    return tasks


def get_random_tasks():
    print('random')
    tasks = []
    for task_type in TASKS_TYPES:
        queryset = DailyTask.objects.filter(task_type=task_type).order_by("?")[:3]
        tasks += list(queryset)
    return tasks


def translate_tasks_in_keyboard(tasks: tuple):
    """Преобразование тупла с заданиями в инлайн клавиатуру"""
    buttons = []
    for index, task in enumerate(tasks):
        selected_or_no = "⛏️" if task.is_selected else ""
        buttons.append(
            ((f"{selected_or_no}{index + 1}|{task.pk}", f"set_to_selected({task.pk})"),)
        )
    keyboard = InlineKeyboard(buttons).keyboard
    return keyboard


def create_daily_task_records(subscriber: Subscriber, tasks):
    result = []
    group = RecordDailyTaskGroup.objects.create()
    for task in tasks:
        r = RecordDailyTask.objects.create(subscriber=subscriber, task=task, group=group)
        result.append(r)
    return result


def get_text(tasks):
    text = ""
    for index, task in enumerate(tasks):
        text += f"{index + 1}) {task.text}\n"
    return text


def send_daily_tasks():
    """Функция рассылает задания для пользователей в кнопках"""
    for subscriber in Subscriber.objects.filter(is_active=True):
        tasks = get_random_tasks()
        text = get_text(tasks)
        
        record_daily_tasks = create_daily_task_records(subscriber, tasks)
        keyboard = translate_tasks_in_keyboard(record_daily_tasks)
        subscriber.up_day()
        Answer(text, keyboard=keyboard, chat_id=subscriber.tg_chat_id).send()


def ask_single_task(tasks_list):
    # tasks_id_list = tasks_list[1:]
    task_record = RecordDailyTask.objects.get(pk=tasks_list[0])
    tasks_id_list = tasks_list[1:]
    text = task_record.task.text
    buttons = [
        (
            ('Да', f'set_to_done({task_record.pk},True,{tasks_id_list})'),
            ('Нет', f'set_to_done({task_record.pk},False,{tasks_id_list})')
        )
    ]
    return text, InlineKeyboard(buttons).keyboard

        
def ask_about_task():
    """Функция рассылает вопросы о выполнении заданий"""
    for subscriber in Subscriber.objects.filter(is_active=True):
        today = timezone.now().date()
        text = "Время заполнить отчет по заданиям, которые ты выбрал:\n\n"
        tasks = [
            x.pk for x in
            RecordDailyTask.objects.filter(subscriber=subscriber, date=today, is_selected=True)
        ]
        task_text, keyboard = ask_single_task(tasks)
        Answer(text + task_text, keyboard=keyboard, chat_id=subscriber.tg_chat_id).send()