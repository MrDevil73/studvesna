from .config import bot as TgBot
from .message_handler import start_message, list_categories

from .callback_handler import perfomances_by_id_category, list_categories_to_edit, give_choice_score,set_assesment

TgBot.register_message_handler(start_message, regexp='start')
TgBot.register_message_handler(list_categories, regexp='list')

TgBot.register_callback_query_handler(list_categories_to_edit, func=lambda call: call.data == "list")
TgBot.register_callback_query_handler(perfomances_by_id_category, func=lambda call: call.data.startswith('category_'))
TgBot.register_callback_query_handler(give_choice_score, func=lambda call: call.data.startswith('perfomance_'))
TgBot.register_callback_query_handler(set_assesment, func=lambda call: call.data.startswith('myassesmentfor_'))
