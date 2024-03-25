from .config import send_message
from .models import TgUser
from telebot.types import Message
import tgvote.keyboards as MyKeyb


def start_message(mess: Message):
    tg_user=TgUser().create_or_update_user(mess.from_user)
    send_message(mess.chat.id, "Приветствуем! Ожидайте дальнейших указаний")


def list_categories(mess: Message):
    send_message(mess.chat.id, "Выберите нужную категорию:", reply_markup=MyKeyb.categoryes())


