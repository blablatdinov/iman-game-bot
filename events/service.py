from bot_init.models import Subscriber
from bot_init.schemas import Answer


def spam_event(sender, instance, **kwargs):
    "Функция вызывается после сохраненения инстанса модели Event"
    for subscriber in Subscriber.objects.filter(is_active=True):
        event_text = f"<b>{instance.title}</b>\n\n{instance.description}"
        Answer(event_text, chat_id=subscriber.tg_chat_id).send()