from django.db import models
from django.utils import timezone

from game.models import MembersGroup


class Subscriber(models.Model):
    """ Модель подписчика бота """
    tg_chat_id = models.IntegerField(verbose_name="Идентификатор подписчика")
    is_active = models.BooleanField(default=True, verbose_name="Подписан ли польователь на бота")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарй к подписчику")
    members_group = models.ForeignKey(
        MembersGroup, on_delete=models.CASCADE, related_name='subscribers',
        verbose_name="Группа в которой состоит пользователь"
    )
    day = models.IntegerField(default=1, verbose_name="День")
    step = models.CharField(max_length=1000, verbose_name="Шаг пользователя", blank=True, null=True)
    registry_date = models.DateField(default=timezone.now, editable=True)
    points_body = models.IntegerField(default=0, verbose_name="Уровень физ. развития")
    points_soul = models.IntegerField(default=0, verbose_name="Уровень духовного развития")
    points_spirit = models.IntegerField(default=0, verbose_name="Уровень душевного развития")

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
    is_removed = models.BooleanField(default=False, verbose_name="Удалено ли сообщение у пользователя")
    key = models.CharField(max_length=32, blank=True, null=True)
    # TODO добавить __str__ метод

    def tg_delete(self):
        from bot_init.service import tg_delete_message
        tg_delete_message(self.chat_id, self.message_id)
        self.is_removed = True
        self.save()

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