from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from callback_factory import MenuCallback

def get_user_main_btns(*, level: int, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    btns = {
        "Товары 🍕": "catalog",
        "Корзина 🛒": "cart",
        "О нас ℹ️": "about",
        "Оплата 💰": "payment",
        "Доставка 🚕": "shipping"
    }
    for text, menu_name in btns.items():
        if menu_name == 'catalog':
            keyboard.add(
                InlineKeyboardButton(
                    text=text,
                    callback_data=MenuCallback(level=level+1, menu_name=menu_name).pack()
                )
            )
        elif menu_name == 'cart':
            keyboard.add(
                InlineKeyboardButton(
                    text=text,
                    callback_data=MenuCallback(level=3, menu_name=menu_name).pack()
                )
            )
        else:
            keyboard.add(
                InlineKeyboardButton(
                    text=text,
                    callback_data=MenuCallback(level=level, menu_name=menu_name).pack()
                )
            )
    return keyboard.adjust(*sizes).as_markup()



def get_user_catalog_btns(*, level: int, categories: list, sizes: tuple[int] = (2,)):
    kb = InlineKeyboardBuilder()

    kb.add(
        InlineKeyboardButton(
            text='⬅️ Назад',
            callback_data=MenuCallback(level=level-1, menu_name='main').pack()
        )
    )
    kb.add(
        InlineKeyboardButton(
            text='Корзина 🛒',
            callback_data=MenuCallback(level=3, menu_name='cart').pack()
        )
    )
    for c in categories:
        kb.add(
            InlineKeyboardButton(
                text=c.name,
                callback_data=MenuCallback(level=level+1, menu_name=c.name, category=c.id).pack()
            )
        )

    return kb.adjust(*sizes).as_markup()



def get_products_btns(
        *,
        level: int,
        category: int,
        page: int,
        pagination_btns: dict,
        product_id: int,
        sizes: tuple[int] = (2,1)
):
    kb = InlineKeyboardBuilder()

    kb.add(InlineKeyboardButton(text='⬅️ Назад',
            callback_data=MenuCallback(level=level-1, menu_name='catalog').pack()))
    kb.add(InlineKeyboardButton(text='Корзина 🛒',
            callback_data=MenuCallback(level=3, menu_name='cart').pack()))
    kb.add(InlineKeyboardButton(text='Купить 💸',
            callback_data=MenuCallback(level=level, menu_name='add_to_cart', product_id=product_id).pack()))
    
    kb.adjust(*sizes)

    row= []
    for text, menu_name in pagination_btns.items():
        if menu_name == "next":
            row.append(InlineKeyboardButton(text=text,
                        callback_data=MenuCallback(
                            level=level,
                            menu_name=menu_name,
                            category=category,
                            page=page+1
                        ).pack()))
        elif menu_name == "previous":
            row.append(InlineKeyboardButton(text=text,
                        callback_data=MenuCallback(
                            level=level,
                            menu_name=menu_name,
                            category=category,
                            page=page-1
                        ).pack()))
    
    return kb.row(*row).as_markup()



def get_user_cart(
        *,
        level: int,
        page: int | None,
        pagination_btns: dict | None,
        product_id: int | None,
        sizes: tuple[int] = (3,)
):
    kb = InlineKeyboardBuilder()
    if page:
        kb.add(InlineKeyboardButton(text='Удалить',
                callback_data=MenuCallback(level=level, menu_name='delete', product_id=product_id, page=page).pack()))
        kb.add(InlineKeyboardButton(text='-1',
                callback_data=MenuCallback(level=level, menu_name='decrement', product_id=product_id, page=page).pack()))
        kb.add(InlineKeyboardButton(text='+1',
                callback_data=MenuCallback(level=level, menu_name='increment', product_id=product_id, page=page).pack()))
        kb.adjust(*sizes)

        row = []
        for text, menu_name in pagination_btns.items():
            if menu_name == 'next':
                row.append(InlineKeyboardButton(text=text,
                            callback_data=MenuCallback(level=level, menu_name=menu_name, page=page+1).pack()))
            elif menu_name == 'previous':
                row.append(InlineKeyboardButton(text=text,
                            callback_data=MenuCallback(level=level, menu_name=menu_name, page=page-1).pack()))
        kb.row(*row)

        row2 = [
            InlineKeyboardButton(text='На главную 🏠',
            callback_data=MenuCallback(level=0, menu_name='main').pack()),
            
            InlineKeyboardButton(text='Заказать',
            callback_data=MenuCallback(level=0, menu_name='order').pack())
        ]
        return kb.row(*row2).as_markup()
    else:
        kb.add(
            InlineKeyboardButton(text='На главную 🏠',
            callback_data=MenuCallback(level=0, menu_name='main').pack()),
        )
        return kb.adjust(*sizes).as_markup()

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



# def get_url_btns(
#     *,
#     btns: dict[str,str],
#     sizes: tuple[int] = (2,)
# ):
#     kb = InlineKeyboardBuilder()

#     for text, url in btns.items():
#         kb.add(
#             InlineKeyboardButton(text=text, url=url)
#         )
    
#     return kb.adjust(*sizes).as_markup()

# def get_inlineMix_btns(
#     *,
#     btns: dict[str,str],
#     sizes: tuple[int] = (2,)
# ):
#     kb = InlineKeyboardBuilder()

#     for text,value in btns.items():
#         if '://' in value:
#             kb.add(InlineKeyboardButton(text=text, url=value))
#         else:
#             kb.add(InlineKeyboardButton(text=text, callback_data=value))

#     return kb.adjust(*sizes).as_markup()
