class Answer:
    text = str

    def __init__(self, text):
        self.text = text

    def send(self, chat_id: int):
        from bot_init.service import get_tbot_instance
        from bot_init.utils import save_message
        tbot = get_tbot_instance()
        message = tbot.send_message(chat_id=chat_id, text=self.text)
        save_message(message)
