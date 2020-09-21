from django.db import models


class MembersGroup(models.Model):
    """Группа участников"""
    title = models.CharField(max_length=200, verbose_name="Название группы")

    class Meta:
        verbose_name = "Группа участников"
        verbose_name_plural = "Группы участников"


class PointsRecord(models.Model):
    """Модель записи пользователя о кол-ве очков"""
    subscriber = models.ForeignKey('bot_init.Subscriber', on_delete=models.CASCADE)
    points_count = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

