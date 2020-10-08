from django.db import models

from game.schemas import DAILY_TASK_TYPE, WEEK_DAYS


class MembersGroup(models.Model):
    """Группа участников"""
    title = models.CharField(max_length=200, verbose_name="Название группы")

    class Meta:
        verbose_name = "Группа участников"
        verbose_name_plural = "Группы участников"


class PointsRecord(models.Model):  # TODO возможно следует убрать
    """Модель записи пользователя о кол-ве очков"""
    subscriber = models.ForeignKey('bot_init.Subscriber', on_delete=models.CASCADE)
    points_count = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)


class DailyTask(models.Model):
    """Задания, приходящие с утра на выполнение"""
    task_type = models.CharField(max_length=16, choices=DAILY_TASK_TYPE)
    text = models.TextField()
    week_day = models.CharField(max_length=5, choices=WEEK_DAYS)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Задание для участников"
        verbose_name_plural = "Задания для участников"


class RecordDailyTaskGroup(models.Model):
    ...


class RecordDailyTask(models.Model):
    """
    Запись о ежедневном задании. Нужно чтобы сохранять, какие задания пользователь выбрал для 
    исполнения.

    """
    subscriber = models.ForeignKey("bot_init.Subscriber", on_delete=models.CASCADE, related_name="daily_tasks_records")
    task = models.ForeignKey(DailyTask, on_delete=models.CASCADE, related_name="daily_tasks_records")
    is_selected = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    complexity = models.IntegerField(default=0, verbose_name="Сложность, которую выбрал пользователь")
    group = models.ForeignKey(RecordDailyTaskGroup, on_delete=models.CASCADE, related_name="daily_tasks_records")

    def switch(self):
        self.is_selected = not self.is_selected
        self.save()

    def set_done(self):
        self.is_done = True
        self.save()


class BeginSurveyQuestion(models.Model):
    """Вопросы для начального тестирования"""
    type = models.CharField(max_length=16, choices=DAILY_TASK_TYPE, verbose_name="Категория вопроса")
    text = models.CharField(max_length=1000, verbose_name="Текст вопроса")

    class Meta:
        verbose_name = "Вопрос для начального тестирования"
        verbose_name_plural = "Вопросы для начального тестирования"


class Reminder(models.Model):
    text = models.TextField()