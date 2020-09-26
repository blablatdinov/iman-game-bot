from django.db import models
from game.models import MembersGroup


class Subscriber(models.Model):
    """ Модель подписчика бота """
    tg_chat_id = models.IntegerField(verbose_name="Идентификатор подписчика")
    is_active = models.BooleanField(default=True, verbose_name="Подписан ли польователь на бота")
    comment = models.TextField(blank=True, null=True)
    members_group = models.ForeignKey(MembersGroup, on_delete=models.CASCADE, related_name='subscribers')
    day = models.IntegerField(default=1)

    def up_day(self):
        self.day += 1
        self.save()

    def __str__(self):
        return str(self.tg_chat_id)

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"


class Message(models.Model):
    """ Модель для хранения сообщеинй """
    date = models.DateTimeField(null=True, verbose_name="Дата отправки")
    from_user_id = models.IntegerField(verbose_name="Идентификатор отправителя")
    message_id = models.IntegerField(verbose_name="Идентификатор сообщения")
    chat_id = models.IntegerField(verbose_name="Идентификатор чата, в котором идет общение")
    text = models.TextField(null=True, verbose_name="Текст сообщения")
    json = models.TextField()

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class AdminMessage(models.Model):
    """Административные сообщения"""
    title = models.CharField(max_length=128, verbose_name='Навзвание')
    text = models.TextField(verbose_name='Текст сообщения')
    key = models.CharField(max_length=128, verbose_name='Ключ, по которому сообщение вызывается в коде')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Админитративное сообщение'
        verbose_name_plural = 'Админитративное сообщения'