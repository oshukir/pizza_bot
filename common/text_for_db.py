from aiogram.utils.formatting import Bold, as_list, as_marked_section

categories = ['Еда', 'Напитки']

description_for_info_pages = {
    'main': 'Добро пожаловать!',
    'about': 'Пиццерия QazPiz.\nРежим работы - 24/7',
    "payment": as_marked_section(
        Bold("Варианты оплаты"),
        "Картой в боте",
        "При получении карта/кэш",
        "В заведении",
        marker="✅ "
    ).as_html(),
    "shipping": as_list(
        as_marked_section(
            Bold("Варианты доставки/заказа:"),
            "Курьер",
            "Самовынос (сейчас прибегу заберу)",
            "Покушаю у Вас (сейчсас прибегу)",
            marker ="✅ "
        ),
        as_marked_section(
            Bold("Нельзя: "),
            "Почта",
            "Голуби",
            marker="❌ "
        ),
        sep="\n--------------------\n"
    ).as_html(),
    'catalog': 'Категории',
    'cart': 'В корзине ничего нет!'
}