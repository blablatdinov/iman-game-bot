"""
Логика для статисктики

"""
import io
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

from bot_init.models import Subscriber
from bot_init.service import get_subscriber_by_chat_id, get_tbot_instance
from game.models import RecordDailyTask


def get_tasks(subscriber: Subscriber):
    now_date = datetime.now()
    start_date = datetime(now_date.year, now_date.month, 1)
    end_date = datetime(now_date.year, (now_date.month + 1 % 12), 1)
    queryset = RecordDailyTask.objects.filter(
        subscriber=subscriber,
        date__range=(start_date, end_date),
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
                    xy=(rect.get_x() + rect.get_width() / 2, height ),
                    xytext=(0, 0),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
    for rect in rects2:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height ),
                    xytext=(0, 0),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return buf


def make_statistic(chat_id: int):
    subscriber = get_subscriber_by_chat_id(chat_id)
    body_record_daily_tasks, soul_record_daily_tasks, spirit_record_daily_tasks = get_tasks(subscriber)
    start_body, start_soul, start_spirit = get_previous_month_result(subscriber)
    end_body = start_body
    end_soul = start_soul
    end_spirit = start_spirit
    for elem in body_record_daily_tasks:
        end_body += elem.complexity
    for elem in soul_record_daily_tasks:
        end_soul += elem.complexity
    for elem in spirit_record_daily_tasks:
        end_spirit += elem.complexity
    start_means = [start_body / 10, start_soul / 10, start_spirit / 10]
    end_means = [end_body / 10, end_soul / 10, end_spirit / 10]
    image = get_plot(start_means, end_means)
    tbot = get_tbot_instance()
    tbot.send_photo(chat_id, image)
