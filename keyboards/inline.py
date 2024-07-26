from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_callback_btns(
    *,
    btns: dict[str,str],
    sizes: tuple[int] = (2,)
):
    kb= InlineKeyboardBuilder()
    
    for text,data in btns.items():
        kb.add(
            InlineKeyboardButton(
                text=text,
                callback_data=data
            )
        )

    return kb.adjust(*sizes).as_markup()

def get_url_btns(
    *,
    btns: dict[str,str],
    sizes: tuple[int] = (2,)
):
    kb = InlineKeyboardBuilder()

    for text, url in btns.items():
        kb.add(
            InlineKeyboardButton(text=text, url=url)
        )
    
    return kb.adjust(*sizes).as_markup()

def get_inlineMix_btns(
    *,
    btns: dict[str,str],
    sizes: tuple[int] = (2,)
):
    kb = InlineKeyboardBuilder()

    for text,value in btns.items():
        if '://' in value:
            kb.add(InlineKeyboardButton(text=text, url=value))
        else:
            kb.add(InlineKeyboardButton(text=text, callback_data=value))

    return kb.adjust(*sizes).as_markup()
