import traceback

import telebot
import os


class MyExceptionHandler(telebot.ExceptionHandler):
    def handle(self, exception: Exception):
        """
        :param exception:
        """
        #print(exception)
        #print(traceback.format_exc())
        pass


bot = telebot.TeleBot(os.getenv("STUDVESNA_TG"), exception_handler=MyExceptionHandler())


def send_message(chat, message, reply_markup=None, parse=None,rep_id=0):
    """Send message to telegram"""
    try:
        bot.send_message(chat_id=chat,
                         text=message,
                         reply_markup=reply_markup,
                         parse_mode=parse if parse else None,
                         disable_web_page_preview=True,
                         reply_parameters=telebot.types.ReplyParameters(message_id=rep_id)
                         )
    except Exception as ex:
        pass


def edit_message(chat, message_id, message, reply_markup=None):
    """Edit message to telegram"""
    try:
        bot.edit_message_text(chat_id=chat, message_id=message_id, text=message, reply_markup=reply_markup, parse_mode="HTML", disable_web_page_preview=True)
    except Exception as ex:
        pass
        #print(ex)
