from bot_init.models import Subscriber
from game.models import MembersGroup


def get_primary_key_from_start_message(text: str) -> int:
    return int(text[7:])


def registration_subscriber(chat_id: int, text: str):
    """Логика сохранения подписчика"""
    subscriber, created = Subscriber.objects.get_or_create(tg_chat_id=chat_id)
    pk = get_primary_key_from_start_message(text)
    subscriber.members_group = MembersGroup.objects.get(pk=pk)
