from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from .models import Category, Performance


def categoryes() -> InlineKeyboardMarkup:
    elements = Category.objects.all().order_by('name_category')
    keyb = InlineKeyboardMarkup()

    for el in elements:
        keyb.row(InlineKeyboardButton(el.name_category.title(), callback_data=f"category_{el.id}"))
    return keyb


def perfomances_by_category(perf: list[Performance], have_score_perf: dict) -> InlineKeyboardMarkup:
    keyb = InlineKeyboardMarkup()
    for el in perf:
        #print(el.id)
        btn_name = f"{el.title_name} | {el.executor} | {have_score_perf.get(el.id,"(Нет оценки)")}"

        keyb.row(InlineKeyboardButton(btn_name, callback_data=f"perfomance_{el.id}"))
    keyb.row(InlineKeyboardButton("↩️ Вернуться", callback_data=f"list"))

    return keyb


def score_keyboard(id_perf: int) -> InlineKeyboardMarkup:
    keyb = InlineKeyboardMarkup()
    for i in range(1, 11):
        keyb.row(InlineKeyboardButton(f"{i}", callback_data=f"myassesmentfor_{id_perf}_{i}"))
    return keyb
