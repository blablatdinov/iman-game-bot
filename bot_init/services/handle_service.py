from django.utils import timezone
from loguru import logger

from bot_init.markup import get_default_keyboard
from bot_init.models import Subscriber, AdminMessage
from bot_init.schemas import Answer
from bot_init.utils import tg_delete_message, get_subscriber_by_chat_id
from config.settings import TIME_LIMITS_FOR_SELECT_TASKS
from game.models import RecordDailyTask, RecordDailyTaskGroup
from game.service import translate_tasks_in_keyboard, ask_single_task
from game.services.survey import set_points, get_next_question, start_survey

log = logger.bind(task="app")


def set_task_to_selected_or_unselected(record_daily_task_id, level, chat_id):
    record_daily_task = RecordDailyTask.objects.get(pk=record_daily_task_id)
    if not(TIME_LIMITS_FOR_SELECT_TASKS[0] <= (timezone.now().hour + 3) % 24 <= TIME_LIMITS_FOR_SELECT_TASKS[1]):
        log.info("This time is not suitable for selecting a task")
        return
    record_task_group = record_daily_task.group
    task_type = record_daily_task.task.task_type
    record_daily_task.switch(level)
    tasks = record_task_group.daily_tasks_records.filter(task__task_type=task_type)
    # TODO выхардкодить индексы
    text = f"{tasks[0].task.get_task_type_display()}\n\n" \
           f"1) {tasks[0].task.text}\n" \
           f"2) {tasks[1].task.text}\n" \
           f"3) {tasks[2].task.text}\n"
    return Answer(text, keyboard=translate_tasks_in_keyboard(tasks), chat_id=chat_id)


def set_task_to_done(task_id, task_status, next_tasks_list, chat_id, message_id):
    if task_status:
        task = RecordDailyTask.objects.get(pk=task_id)
        task.set_done()
    if len(next_tasks_list) == 0:
        subscriber = Subscriber.objects.get(tg_chat_id=chat_id)
        text = AdminMessage.objects.get(key="other_day_survey").text
        if subscriber.day == 1:
            subscriber.day = 2
            subscriber.save()
        else:
            ...
        tg_delete_message(chat_id=chat_id, message_id=message_id)
        Answer(text, keyboard=get_default_keyboard(), chat_id=chat_id).send()
        return
    text, keyboard = ask_single_task(next_tasks_list)
    return Answer(text, keyboard=keyboard, chat_id=chat_id)


def begin_survey(value, begin_question_pk, chat_id):
    from bot_init.service import get_acquaintance_next_keyboard
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


def acquaintance(chat_id, step_num):
    from bot_init.service import get_acquaintance_next_keyboard
    if step_num == 5:
        admin_message = AdminMessage.objects.get(pk=step_num + 1)
        Answer(admin_message.text, keyboard=get_default_keyboard(), chat_id=chat_id).send()
        subscriber = get_subscriber_by_chat_id(chat_id)
        subscriber.step = ""
        subscriber.save()
        text = 'Начальные данные:\n\n' \
               f'Тело: {subscriber.points_body}\n' \
               f'Душа: {subscriber.points_spirit}\n' \
               f'Дух: {subscriber.points_soul}'
        Answer(text, keyboard=get_default_keyboard(), chat_id=chat_id).send()
        return
    elif step_num == 2:
        answer = start_survey(chat_id)
        return answer
    admin_message = AdminMessage.objects.get(pk=step_num + 1)
    text = admin_message.text
    keyboard = get_acquaintance_next_keyboard(step_num + 1)
    Answer(text, keyboard=keyboard, chat_id=chat_id).send()


def get_task_keyboard(chat_id, task_type, group_pk):
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
