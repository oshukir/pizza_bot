from aiogram import F, Router, types
from aiogram.filters import Command, or_f
from filters.chat_types import ChatTypeFilter, IsAdmin
from keyboards.reply import get_keyboard
from states import Addproduct
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, any_state

from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Product
from database.orm_query import (
    orm_add_product,
    orm_delete_produce,
    orm_get_products,
    orm_get_product,
    orm_update_product
)

from keyboards.inline import (
    get_callback_btns
)

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(['private']), IsAdmin())

ADMIN_KB = get_keyboard(
    "Добавить товар",
    "Ассортимент",
    placeholder="Выберите действие",
    sizes=(2,)
)

@admin_router.message(Command("admin"))
async def add_produce(message: types.Message):
    await message.answer(text="Что хотите сделать?", reply_markup=ADMIN_KB)

@admin_router.message(F.text == "Ассортимент")
async def starring_at_product(message: types.Message, session: AsyncSession):
    for product in await orm_get_products(session=session):
        await message.answer_photo(
            product.image,
            caption=f"{product.name}\n{product.description}\nСтоимость:{round(product.price, 2)} тг",
            reply_markup=get_callback_btns(
                btns={
                    'Удалить' : f"delete_{product.id}",
                    'Изменить' : f'change_{product.id}'
                }
            )
        )
    await message.answer("Ок, вот список товаров ⬆️")




@admin_router.message(default_state, F.text == "Добавить товар")
async def add_product(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите название товара", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(Addproduct.name)


@admin_router.message(any_state, Command("отмена"))
@admin_router.message(any_state, F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Действия отменены", reply_markup=ADMIN_KB)

@admin_router.message(any_state, Command("назад"))
@admin_router.message(any_state, F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()

    if current_state == Addproduct.name:
        await message.answer('Предидущего шага нет, или введите название товара или напишите "отмена"')
        return

    previous = None
    for step in Addproduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Ок, вы вернулись к прошлому шагу \n {Addproduct.texts[previous.state]}")
            return
        previous = step


@admin_router.message(Addproduct.name, or_f(F.text,F.text == '.'))
async def add_name(message: types.Message, state: FSMContext):
    if message.text == ".":
        await state.update_data(name=Addproduct.product_for_change.name)
    else:
        if len(message.text) >= 100:
            await message.answer("Название товара не должно превышать 100 символов. \n Введите заново")
            return
    
        await state.update_data(name=message.text)
    await message.answer("Введите описание товара")
    await state.set_state(Addproduct.description)

@admin_router.message(Addproduct.name)
async def add_name2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, введите текст названия товара")



@admin_router.message(Addproduct.description, or_f(F.text,F.text == '.'))
async def add_description(message: types.Message, state: FSMContext):
    if message.text == ".":
        await state.update_data(description=Addproduct.product_for_change.description)
    else:
        await state.update_data(description=message.text)
    await message.answer("Введите стоимость товара")
    await state.set_state(Addproduct.price)

@admin_router.message(Addproduct.description)
async def add_description2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, введите текст описания товара")


@admin_router.message(Addproduct.price, or_f(F.text, F.text == '.'))
async def add_price(message: types.Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(price=Addproduct.product_for_change.price)
    else:
        try:
            float(message.text)
        except ValueError:
            await message.answer("Введите корректное значение цены")
            return
        await state.update_data(price=message.text)
    await message.answer("Загрузите изображение товара")
    await state.set_state(Addproduct.image)


@admin_router.message(Addproduct.price)
async def add_price2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, введите стоимость товара")




@admin_router.message(Addproduct.image, or_f(F.photo, F.text == "."))
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):
    if message.text and message.text == ".":
        await state.update_data(image=Addproduct.product_for_change.image)

    else:
        await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()
    try:
        if Addproduct.product_for_change:
            await orm_update_product(session, Addproduct.product_for_change.id, data)
        else:
            await orm_add_product(session, data)
        await message.answer("Товар добавлен/изменен", reply_markup=ADMIN_KB)
        await state.clear()

    except Exception as e:
        await message.answer(
            f"Ошибка: \n{str(e)}\nОбратись к программеру, он опять денег хочет",
            reply_markup=ADMIN_KB,
        )
        await state.clear()

    Addproduct.product_for_change = None


@admin_router.message(Addproduct.image)
async def add_image2(message: types.Message, state: FSMContext):
    await message.answer("Отправьте фото пищи")