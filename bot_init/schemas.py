# TODO жирные методы
from bot_init.markup import get_default_keyboard


class Answer:
    text = str
    keyboard = get_default_keyboard()
    chat_id: int

    def __init__(self, text, chat_id: int = None, keyboard=None, message_key=None):
        self.text = text
        if keyboard is not None:
            self.keyboard = keyboard
        if chat_id is not None:
            self.chat_id = chat_id
        self.message_key = message_key

    def send(self, chat_id: int = None):
        from bot_init.service import get_tbot_instance
        from bot_init.utils import save_message
        if chat_id is None:
            chat_id = self.chat_id
        if chat_id is None:
            raise Exception("Не передан идентификатор чата")
        tbot = get_tbot_instance()
        try:
            if self.keyboard:
                message = tbot.send_message(chat_id=chat_id, text=self.text, reply_markup=self.keyboard, parse_mode="HTML")
                save_message(message, message_key=self.message_key)
                return
            message = tbot.send_message(chat_id=chat_id, text=self.text, parse_mode="HTML")
            save_message(message, message_key=self.message_key)
        except Exception as e:
            print(e)

    def edit(self, message_id: int, chat_id: int = None):
        from bot_init.service import get_tbot_instance
        from bot_init.utils import save_message
        if chat_id is None:
            chat_id = self.chat_id
        if chat_id is None:
            raise Exception("Не передан идентификатор чата")
        tbot = get_tbot_instance()
        try:
            if self.keyboard:
                message = tbot.edit_message_text(
                    chat_id=chat_id, 
                    message_id=message_id,
                    text=self.text, 
                    reply_markup=self.keyboard, 
                    parse_mode="HTML"
                )
                return
            message = tbot.send_message(chat_id=chat_id, text=self.text, parse_mode="HTML")
            save_message(message)
        except Exception as e:
            print(e)

