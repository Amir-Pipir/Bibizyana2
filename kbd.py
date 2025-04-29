from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Dict, Tuple

phone_button = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Отправить свой контакт ☎️', request_contact=True),
    ]
],
    resize_keyboard=True, one_time_keyboard=True)

remove = ReplyKeyboardRemove()


def inline_kb(
        *,
        btns: Dict[str, str],
        sizes: Tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():
        if "://" in data:
            keyboard.add(InlineKeyboardButton(text=text, url=data))
        else:
            keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()


def reply_kb(*, btns):
    keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=text) for text in row] for row in btns],
                                   resize_keyboard=True, one_time_keyboard=True)
    return keyboard
