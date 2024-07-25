from aiogram import types, F, Router
from aiogram.types import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_keyboard(
    *btns: str,
    placeholder: str = None,
    request_contact: int = None,
    request_location: int = None,
    sizes: tuple[int] = (2,)
):
    kb = ReplyKeyboardBuilder()

    for index, text in enumerate(btns, start=0):
        if request_contact == index:
            kb.add(KeyboardButton(
                text=text,
                request_contact=True
            ))
        elif request_location == index:
            kb.add(KeyboardButton(
                text=text,
                request_location=True
            ))
        else:
            kb.add(KeyboardButton(
                text=text
            ))

    kb.adjust(*sizes)
    return kb.as_markup(placeholder=placeholder, resize_keyboard=True)
