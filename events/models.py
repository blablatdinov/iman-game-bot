from django.db import models
from django.db.models.signals import post_save

from events.service import spam_event


class Event(models.Model):
    """ Модель события """
    title = models.CharField(max_length=64, verbose_name='Название события')
    description = models.TextField(verbose_name='Описание события')
    sending_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'


post_save.connect(spam_event, Event)