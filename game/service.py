from datetime import datetime

from django.utils import timezone
from loguru import logger

from bot_init.models import Subscriber, Message
from bot_init.markup import InlineKeyboard
from bot_init.schemas import Answer
from game.schemas import DAILY_TASK_TYPE, WEEK_DAYS
from game.models import DailyTask, RecordDailyTask, RecordDailyTaskGroup, Reminder

TASKS_TYPES = tuple([x[0] for x in DAILY_TASK_TYPE])
log = logger.bind(task="app")


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
        return "💪"
    return ""


def translate_tasks_in_keyboard(tasks: tuple):
    """Преобразование тупла с заданиями в инлайн клавиатуру"""
    task_type = tasks[0].task.task_type
    task_group_pk = tasks[0].group.pk
    buttons = []
    for index, task in enumerate(tasks):
        if RecordDailyTask.objects.get(pk=task.pk).is_selected:
            action_name = "set_to_unselected"
        else:
            action_name = "set_to_selected"
        buttons.append(
            (
                (f"{selected_or_no(task.pk, 1)} 1", f"{action_name}({task.pk},1)"),
                (f"{selected_or_no(task.pk, 2)} 2", f"{action_name}({task.pk},2)"),
                (f"{selected_or_no(task.pk, 3)} 3", f"{action_name}({task.pk},3)"),
            )
        )
    if task_type == "body":
        buttons.append((("Душа >", f"get_task_keyboard('soul', {task_group_pk})"),))
    elif task_type == "soul":
        buttons.append(
            (("< Тело", f"get_task_keyboard('body', {task_group_pk})"), ("Дух >", f"get_task_keyboard('spirit', {task_group_pk})"),)
        )
    elif task_type == "spirit":
        buttons.append(
            (("< Душа", f"get_task_keyboard('soul', {task_group_pk})"),)
        )
    keyboard = InlineKeyboard(buttons).keyboard
    return keyboard


def create_daily_task_records(subscriber: Subscriber, tasks):
    group = RecordDailyTaskGroup.objects.create()
    for task in tasks:
        r = RecordDailyTask.objects.create(subscriber=subscriber, task=task, group=group)
    return group


def get_text(tasks):
    text = ""
    for index, task in enumerate(tasks):
        text += f"{index + 1}) {task.text}\n"
    return text


def get_week_day():
    return WEEK_DAYS[datetime.today().weekday()][0]


def send_daily_tasks():
    """
    Функция рассылает задания для пользователей в кнопках.
    Происходит отправка заданий категории body с клавиатурой для переключения на другие категории

    """
    week_day = get_week_day()
    tasks = DailyTask.objects.filter(week_day=week_day)
    text = get_text(tasks.filter(task_type="body"))
    for subscriber in Subscriber.objects.filter(is_active=True):  # TODO вынести итерацию в отдельную функцию, чтобы пользователю можно было отправлять индивидуально
        group = create_daily_task_records(subscriber, tasks)
        body_tasks = group.daily_tasks_records.filter(task__task_type="body")
        keyboard = translate_tasks_in_keyboard(body_tasks)
        Answer(text, keyboard=keyboard, chat_id=subscriber.tg_chat_id, message_key="ques_tasks").send()


def ask_single_task(tasks_list):
    task_record = RecordDailyTask.objects.get(pk=tasks_list[0])
    tasks_id_list = tasks_list[1:]
    text = task_record.task.text
    buttons = [
        (
            ('Да', f'settodone({task_record.pk},True,{tasks_id_list})'.replace(" ", "")),
            ('Нет', f'settodone({task_record.pk},False,{tasks_id_list})'.replace(" ", ""))
        )
    ]
    return text, InlineKeyboard(buttons).keyboard


def ask_about_task():
    """Функция рассылает вопросы о выполнении заданий"""
    # TODO сделать функцию вызываемой для одного человека
    # TODO формируемая инфа для кнопок слишком длинная
    log.info("Starting to collect the report of selected tasks")
    for subscriber in Subscriber.objects.filter(is_active=True):
        log.info(f"send report blank to {subscriber.tg_chat_id}")
        today = timezone.now().date()
        if subscriber.day == 1:
            text = "Ну что, по основным моментам мы с тобой прошлись. Если остались вопросы, " \
                   "то задавай их в нашем Telegam чате tg://join?invite=AAAAAEaDF5qIQRwLVR59cQ " \
                   "или на странице в Инстаграм @iman.club На этом все, ты выполняй задания, " \
                   "я буду их анализировать и через месяц покажу на сколько ты прибавил в " \
                   "каждом пункте своего развития. Алга, брат! Бисмиллях!\n\n"
        else:
            text = "И снова, Ас-саляму ‘алейкум, брат! Как прошел день? Что из запланированного получилось сделать? " \
                   "Поделись со мной и я внесу твой результат в наш отчет.\n\n"
        tasks = [
            x.pk for x in
            RecordDailyTask.objects.filter(subscriber=subscriber, date=today, is_selected=True)
        ]
        if len(tasks) < 1:
            log.info(f"{subscriber.tg_chat_id} no select task")
            continue
        task_text, keyboard = ask_single_task(tasks)
        Answer(text + task_text, keyboard=keyboard, chat_id=subscriber.tg_chat_id, message_key="ask_about_tasks").send()


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


def clean_messages(key):
    log.info(f"cleaning message with key - {key}")
    queryset = Message.objects.filter(key=key)
    for message in queryset:
        try:
            message.tg_delete()
            log.info(f"delete message id - {message.message_id}")
        except Exception as e:
            print(e)


def send_reminders():
    for subscriber in Subscriber.objects.filter(is_active=True):
        reminder_text = Reminder.objects.all().order_by("?")[0].text
        Answer(reminder_text).send(subscriber.tg_chat_id)
        log.info(f"Send reminders {reminder_text} to {subscriber.tg_chat_id}")


def send_list_with_selected_tasks():
    for subscriber in Subscriber.objects.filter(is_active=True):
        text = ""
        try:
            today = timezone.now()
            tasks = RecordDailyTask.objects.filter(
                date__day=today.day,
                date__month=today.month,
                date__year=today.year,
                subscriber=subscriber,
                is_selected=True
            )
            for i, st in enumerate(tasks.filter(subscriber=subscriber, is_selected=True)):
                text += f"{i + 1}. {st.task.text} ({st.task.get_task_type_display()})\n"
            log.info(f"Send list of tasks ({text}) to {subscriber.tg_chat_id}")
            Answer(text=text).send(subscriber.tg_chat_id)
        except Exception as e:
            log.error(str(e))
