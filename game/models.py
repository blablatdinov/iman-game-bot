from django.db import models


class MembersGroup(models.Model):
    """Группа участников"""
    title = models.CharField(max_length=200, verbose_name="Название группы")

    class Meta:
        verbose_name = "Группа участников"
        verbose_name_plural = "Группы участников"
