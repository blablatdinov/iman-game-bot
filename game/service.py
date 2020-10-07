from datetime import datetime

from django.utils import timezone

from bot_init.models import Subscriber, Message
from bot_init.markup import InlineKeyboard
from bot_init.schemas import Answer
from game.schemas import DAILY_TASK_TYPE, WEEK_DAYS
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
    tasks = []
    for task_type in TASKS_TYPES:
        queryset = DailyTask.objects.filter(task_type=task_type).order_by("?")[:3]
        tasks += list(queryset)
    return tasks


def selected_or_no(task_pk, level):
    record_daily_task = RecordDailyTask.objects.get(pk=task_pk)
    if record_daily_task.complexity == level:
        return "⛏️"
    return ""


def translate_tasks_in_keyboard(tasks: tuple):
    """Преобразование тупла с заданиями в инлайн клавиатуру"""
    buttons = []
    for index, task in enumerate(tasks):
        # selected_or_no = "⛏️" if task.is_selected else ""
        buttons.append(
            (
                (f"{selected_or_no(task.pk, 1)}{index + 1}) Уровень: 1", f"set_to_selected({task.pk},{1})"),
                (f"{selected_or_no(task.pk, 2)}{index + 1}) Уровень: 2", f"set_to_selected({task.pk},{2})"),
                (f"{selected_or_no(task.pk, 3)}{index + 1}) Уровень: 3", f"set_to_selected({task.pk},{3})"),
            )
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


def get_week_day():
    return WEEK_DAYS[datetime.today().weekday()][0]


def send_daily_tasks():
    """Функция рассылает задания для пользователей в кнопках"""
    week_day = get_week_day()
    tasks = DailyTask.objects.filter(week_day=week_day)
    text = ""
    text += get_text(tasks)
    for subscriber in Subscriber.objects.filter(is_active=True):
        record_daily_tasks = create_daily_task_records(subscriber, tasks)
        keyboard = translate_tasks_in_keyboard(record_daily_tasks)
        Answer(text, keyboard=keyboard, chat_id=subscriber.tg_chat_id).send()


def ask_single_task(tasks_list):
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
        text = "И снова, Ас-саляму ‘алейкум, брат! Как прошел день? Что из запланированного получилось сделать? " \
               "Поделись со мной и я внесу твой результат в наш отчет. "
        tasks = [
            x.pk for x in
            RecordDailyTask.objects.filter(subscriber=subscriber, date=today, is_selected=True)
        ]
        if len(tasks) < 1:
            continue
        task_text, keyboard = ask_single_task(tasks)
        Answer(text + task_text, keyboard=keyboard, chat_id=subscriber.tg_chat_id).send()


def clean_ask():
    """
    Если пользователь не успел заполнить отчет, то сообщения с приглашением 
    заполнить отчет удаляются
    
    """
    queryset = Message.objects.filter(
        is_removed=False, text__contains="Время заполнить отчет по заданиям, которые ты выбрал"
    )
    for message in queryset:
        try:
            message.tg_delete()
        except Exception as e:
            print(e)
