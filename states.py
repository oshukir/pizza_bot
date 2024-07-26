from aiogram.fsm.state import State, StatesGroup

class Addproduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()

    texts = {
        'Addproduct:name' : 'Введите название заново',
        'Addproduct:description' : 'Введите описание заново',
        'Addproduct:price' : 'Введите стоиомость заново',
        'Addproduct:image' : 'Этот стейт последний, поэтому....'
    }

    product_for_change = None