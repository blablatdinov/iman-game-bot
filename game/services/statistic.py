"""
Логика для статисктики

"""
import io
from datetime import datetime, timedelta

from PIL import Image, ImageDraw, ImageFont
from loguru import logger

from bot_init.models import Subscriber
from bot_init.service import get_subscriber_by_chat_id, get_tbot_instance
from game.models import RecordDailyTask
from math import cos, sin, pi


tbot = get_tbot_instance()
log = logger.bind(task="statistic")


def get_tasks_per_period(subscriber: Subscriber, period):
    start_date = period[0]
    end_date = period[1]
    queryset = RecordDailyTask.objects.filter(
        subscriber=subscriber,
        date__range=(start_date, end_date),
        is_selected=True,
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
    start_spirit = subscriber.points_spirit
    return start_body * 10, start_soul * 10, start_spirit * 10


def get_plot(list1, list2):
    chart = Chart()
    chart.create_empty_chart()
    chart.set_list1_points(list1)
    chart.set_list2_points(list2)
    chart.create_triangles()
    chart.create_text()
    chart.render()
    byte_io = io.BytesIO()
    chart.image.save(byte_io, "PNG")
    return byte_io.getvalue()


def get_plus_per_period(subscriber: Subscriber, period):
    """
    subscriber: Subscriber
    period: tuple(datetime, datetime)
    """
    body_record_daily_tasks, soul_record_daily_tasks, spirit_record_daily_tasks = get_tasks_per_period(subscriber, period)
    result = [0, 0, 0]
    for task in body_record_daily_tasks:
        if task.is_done:
            result[0] += 2
    for task in soul_record_daily_tasks:
        if task.is_done:
            result[1] += 2
    for task in spirit_record_daily_tasks:
        if task.is_done:
            result[2] += 2
    return result


def find_week_day(start_date, week_day_index):
    for i in range(7):
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
            result[0] -= 1
        if tasks[1].filter(
            date__range=(start_date, end_date),
            is_done=False,
            is_selected=True,
        ).count() >= 3:
            result[1] -= 1
        if tasks[2].filter(
            date__range=(start_date, end_date),
            is_done=False,
            is_selected=True,
        ).count() >= 3:
            result[2] -= 1
    return result


def get_nafs_value(subscriber, period):
    result = 0
    tasks = get_tasks_per_period(subscriber, period)
    for group in tasks:
        group = group.filter(is_selected=True, is_done=True)
        for task in group:
            result += task.complexity
    return result


def make_statistic(chat_id: int, period):
    subscriber = get_subscriber_by_chat_id(chat_id)
    start_body, start_soul, start_spirit = get_previous_month_result(subscriber)
    diff_body, diff_soul, diff_spirit = get_plus_per_period(
        subscriber, period
    )
    log.debug(f"{diff_body=} {diff_soul=} {diff_spirit=}")
    start_means = [start_body / 10, start_soul / 10, start_spirit / 10]
    log.debug(f"{start_means=}")
    task_records = get_tasks_per_period(subscriber, period)
    minuses = get_minus_per_skips(subscriber, task_records)
    log.debug(f"{minuses=}")
    end_means = [
        (start_body + diff_body - minuses[0]) / 10,
        (start_soul + diff_soul - minuses[1]) / 10,
        (start_spirit + diff_spirit - minuses[2]) / 10
    ]
    log.debug(f"{end_means=}")
    nafs_value = get_nafs_value(subscriber, period)
    image = get_plot(start_means, end_means)
    # 125821629
    try:
        tbot.send_photo(chat_id, image, caption=f'Воспитание нафса - {round(nafs_value / 10, 1)}')
    except Exception as e:
        print(e)


def make_statistic_by_two_week(chat_id):
    subscriber = get_subscriber_by_chat_id(chat_id)
    log.debug(f"{subscriber}")
    period = (
        # subscriber.registry_date,
        # subscriber.registry_date + timedelta(14)
        datetime(2020, 10, 20),
        datetime(2020, 11, 3),
    )
    make_statistic(chat_id, period)


def make_statistic_by_month(chat_id):
    subscriber = get_subscriber_by_chat_id(chat_id)
    period = (
        subscriber.registry_date,
        subscriber.registry_date + timedelta(30)
    )
    make_statistic(chat_id, period)


CHART_CENTER_COORDS = (600, 600)
IMAGE_SIZE = (1200, 1080)
LINE_LENGTH = 350
LINE_WEIDTH = 10
COLOR1 = (0, 0, 0)
COLOR2 = (245, 202, 20)


class Line:

    def __init__(self, draw: ImageDraw, corner):
        self._draw = draw
        self.corner = corner * pi / 180

    def create(self):
        x1 = CHART_CENTER_COORDS[0]
        y1 = CHART_CENTER_COORDS[1]
        x2 = CHART_CENTER_COORDS[0] + (round(cos(self.corner), 3) * LINE_LENGTH)
        y2 = CHART_CENTER_COORDS[1] + (-round(sin(self.corner), 3) * LINE_LENGTH)
        self.coords = [x1, y1, x2, y2]
        self._draw.line(
            [x1, y1, x2, y2], fill='white', width=LINE_WEIDTH
        )
        return tuple([x1, y1, x2, y2])


class Point:
    coords: list
    diametr = 30

    def __init__(self, draw: ImageDraw, line, value, color):
        self._line = line
        self._draw = draw
        self._value = value
        self._color = color

    def calculate_coords(self):
        x1 = self._line.coords[0]
        y1 = self._line.coords[1]
        x2 = self._line.coords[2]
        y2 = self._line.coords[3]
        x_diff = x2 - x1
        y_diff = y2 - y1
        if not x_diff:
            x_coord = x2
        else:
            x_coord = round(self._value * x_diff / 100) + CHART_CENTER_COORDS[0]
        if not y_diff:
            y_coord = y2
        else:
            y_coord = CHART_CENTER_COORDS[1] + round(self._value * y_diff / 100)
        self.coords = [x_coord, y_coord]
        self._draw.ellipse(
            [
                x_coord - self.diametr / 2,
                y_coord - self.diametr / 2,
                x_coord + self.diametr / 2,
                y_coord + self.diametr / 2,
                ],
            fill=self._color
        )


class Chart:
    lines = []
    image: Image
    draw: ImageDraw

    def __init__(self):
        ...

    def create_empty_chart(self):
        self.image = Image.new("RGBA", IMAGE_SIZE, (82, 82, 82,))
        self.draw = ImageDraw.Draw(self.image)
        self.lines = [
            Line(self.draw, 90),
            Line(self.draw, -30),
            Line(self.draw, -150)
        ]
        for elem in self.lines:
            elem.create()

    def set_list1_points(self, list1):
        self.list1 = list1
        self.first_points_group = [
            Point(self.draw, self.lines[0], list1[0], COLOR1),
            Point(self.draw, self.lines[1], list1[1], COLOR1),
            Point(self.draw, self.lines[2], list1[2], COLOR1),
        ]
        for x in self.first_points_group:
            x.calculate_coords()

    def set_list2_points(self, list2):
        self.list2 = list2
        self.second_points_group = [
            Point(self.draw, self.lines[0], list2[0], COLOR2),
            Point(self.draw, self.lines[1], list2[1], COLOR2),
            Point(self.draw, self.lines[2], list2[2], COLOR2),
        ]
        for x in self.second_points_group:
            x.calculate_coords()

    def create_triangles(self):
        first_triangle = Triangle(self.draw, self.first_points_group, COLOR1)
        second_triangle = Triangle(self.draw, self.second_points_group, COLOR2)
        img = Image.alpha_composite(first_triangle.render(), second_triangle.render())
        self.triangle_images = img
        return img

    def create_text(self):
        diffs = []
        for i in range(3):
            diff = round(self.list2[i] - self.list1[i], 2)
            if diff > 0:
                diffs.append(f"+{diff}")
            elif diff <= 0:
                diffs.append(f"{diff}")
        font = ImageFont.truetype("sans-serif.ttf", 60)
        self.draw.text((430 + 20, 200 - 40), f"Тело ({diffs[0]})", (255, 255, 255), font=font)
        self.draw.text((763 + 40, 845 - 60), f"Душа ({diffs[1]})", (255, 255, 255), font=font)
        self.draw.text((96 + 40, 845 - 60), f"Дух ({diffs[2]})", (255, 255, 255), font=font)

    def render(self):
        self.image = Image.alpha_composite(self.image, self.triangle_images)
        self.image.save("image.png")


class Triangle:

    def __init__(self, draw, points_group, color):
        self._draw = draw
        self._points_group = points_group
        self._color = color

    def create_edges(self):
        for x in range(3):
            self._draw.line(
                [
                    self._points_group[x].coords[0],
                    self._points_group[x].coords[1],
                    self._points_group[(x + 1) % 3].coords[0],
                    self._points_group[(x + 1) % 3].coords[1],
                ],
                fill=self._color,
                width=10
            )

    def render(self):
        image = Image.new("RGBA", IMAGE_SIZE, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        fill = list(self._color)
        fill.append(100)
        self.create_edges()
        peak_coords = [
            (self._points_group[0].coords[0], self._points_group[0].coords[1]),
            (self._points_group[1].coords[0], self._points_group[1].coords[1]),
            (self._points_group[2].coords[0], self._points_group[2].coords[1]),
        ]
        draw.polygon(peak_coords, fill=tuple(fill))
        return image
