from aiogram.fsm.state import State, StatesGroup

class Addproduct(StatesGroup):
    name = State()
    description = State()
    category = State()
    price = State()
    image = State()

    texts = {
        'Addproduct:name' : 'Введите название заново',
        'Addproduct:description' : 'Введите описание заново',
        'Addproduct:category' : 'Выберите категорию заново ⤴️',
        'Addproduct:price' : 'Введите стоиомость заново',
        'Addproduct:image' : 'Этот стейт последний, поэтому....'
    }

    product_for_change = None


class Addbanner(StatesGroup):
    image = State()