"""
Логика для статисктики

"""
import io
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
from loguru import logger

from bot_init.models import Subscriber
from bot_init.utils import get_subscriber_by_chat_id
from bot_init.utils import get_tbot_instance
from game.models import RecordDailyTask


def get_tasks_per_period(subscriber: Subscriber, period):  # TODO поменять название ф-ии на get_doned_tasks_per_period
    start_date = period[0]
    end_date = period[1]
    queryset = RecordDailyTask.objects.filter(
        subscriber=subscriber,
        date__range=(start_date, end_date),
        is_done=True
    )
    result = (
        queryset.filter(task__task_type="body"),
        queryset.filter(task__task_type="soul"),
        queryset.filter(task__task_type="spirit"),
    )
    return result


def get_previous_month_result(subscriber: Subscriber):
    start_body = subscriber.points_body
    start_soul = subscriber.points_soul
    start_spirit = subscriber.points_body
    return start_body * 10, start_soul * 10, start_spirit * 10


def get_plot(start_means: list, end_means: list):
    labels = ['Здоровье', 'Личностный рост', 'Духовное развитие']
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, start_means, width, label='Прошлый месяц')
    rects2 = ax.bar(x + width / 2, end_means, width, label='Сегодня')
    ax.set_ylabel('Баллы')
    ax.set_title('Прогресс за месяц')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    for rect in rects1:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 0),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
    for rect in rects2:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 0),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return buf


def get_plus_per_period(subscriber: Subscriber, period):
    """
    subscriber: Subscriber
    period: tuple(datetime, datetime)
    """
    body_record_daily_tasks, soul_record_daily_tasks, spirit_record_daily_tasks = get_tasks_per_period(subscriber, period)
    result = [0, 0, 0]
    for _ in body_record_daily_tasks:
        result[0] += 2
    for _ in soul_record_daily_tasks:
        result[1] += 2
    for _ in spirit_record_daily_tasks:
        result[2] += 2
    return result


def find_week_day(start_date, week_day_index):
    for i in range(6):
        if (date_ := start_date + timedelta(i)).weekday() == week_day_index:
            return date_


def get_date_ranges(first_monday, last_sunday):
    result = []
    n = 0
    while True:
        result.append(
            (first_monday + timedelta(days=7 * n), first_monday + timedelta(days=7 * n + 7))
        )
        n += 1
        if first_monday + timedelta(days=7 * n - 1) == last_sunday:
            break
    return result


def get_minus_per_skips(subscriber: Subscriber, tasks):
    result = [0, 0, 0]
    now_date = datetime.now()
    start_date = subscriber.registry_date
    end_date = start_date + timedelta(days=30)
    first_monday = find_week_day(start_date, 0) - timedelta(7)
    last_sunday = find_week_day(end_date, 6)
    ranges = get_date_ranges(first_monday, last_sunday)
    for start_date, end_date in ranges:
        if tasks[0].filter(
            date__range=(start_date, end_date),
            is_done=False,
            is_selected=True,
        ).count() >= 3:
            result[0] -= 1.5
        if tasks[1].filter(
            date__range=(start_date, end_date),
            is_done=False,
            is_selected=True,
        ).count() >= 3:
            result[1] -= 1.5
        if tasks[2].filter(
            date__range=(start_date, end_date),
            is_done=False,
            is_selected=True,
        ).count() >= 3:
            result[2] -= 1.5
    return result


def get_nafs_value(subscriber, period):
    result = 0
    tasks = get_tasks_per_period(subscriber, period)
    for group in tasks:
        group = group.filter(is_selected=True, is_done=True)
        for task in group:
            logger.debug(task)
            logger.debug(task.complexity)
            result += task.complexity
    return result


def make_statistic(chat_id: int, period):
    subscriber = get_subscriber_by_chat_id(chat_id)
    start_body, start_soul, start_spirit = get_previous_month_result(subscriber)
    diff_body, diff_soul, diff_spirit = get_plus_per_period(
        subscriber, period
    )
    start_means = [start_body / 10, start_soul / 10, start_spirit / 10]
    task_records = get_tasks_per_period(subscriber, period)
    minuses = get_minus_per_skips(subscriber, task_records)
    end_means = [
        (start_body + diff_body - minuses[0]) / 10,
        (start_soul + diff_body - minuses[1]) / 10,
        (start_spirit + diff_body - minuses[2]) / 10
    ]
    nafs_value = get_nafs_value(subscriber, period)
    logger.debug(f'nafs value = {nafs_value/10}')
    image = get_plot(start_means, end_means)
    tbot = get_tbot_instance()
    tbot.send_photo(chat_id, image, caption=f'Нафс {nafs_value}')


def make_statistic_by_two_week(chat_id):
    subscriber = get_subscriber_by_chat_id(chat_id)
    period = (
        subscriber.registry_date,
        subscriber.registry_date + timedelta(14)
    )
    make_statistic(chat_id, period)


def make_statistic_by_month(chat_id):
    subscriber = get_subscriber_by_chat_id(chat_id)
    period = (
        subscriber.registry_date,
        subscriber.registry_date + timedelta(30)
    )
    make_statistic(chat_id, period)
