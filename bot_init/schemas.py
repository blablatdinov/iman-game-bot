from bot_init.markup import get_default_keyboard


class Answer:
    text = str
    keyboard = get_default_keyboard()

    def __init__(self, text, keyboard=None):
        self.text = text
        if keyboard is not None:
            self.keyboard = keyboard

    def send(self, chat_id: int):
        from bot_init.service import get_tbot_instance
        from bot_init.utils import save_message
        tbot = get_tbot_instance()
        if self.keyboard:
            message = tbot.send_message(chat_id=chat_id, text=self.text, reply_markup=self.keyboard)
            return
        message = tbot.send_message(chat_id=chat_id, text=self.text)
        save_message(message)
        return
