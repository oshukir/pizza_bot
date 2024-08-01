from aiogram import F, Router, types
from aiogram.filters import Command, or_f
from filters.chat_types import ChatTypeFilter, IsAdmin
from keyboards.reply import get_keyboard
from states import Addproduct, Addbanner
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, any_state

from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Product
from database.orm_query import (
    orm_add_product,
    orm_delete_produce,
    orm_get_products,
    orm_get_product,
    orm_update_product,
    orm_get_categories,
    orm_get_info_pages,
    orm_change_banner_image
)

from keyboards.inline import (
    get_callback_btns
)

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(['private']), IsAdmin())

ADMIN_KB = get_keyboard(
    "Добавить товар",
    "Ассортимент",
    "Добавить/изменить баннер",
    placeholder="Выберите действие",
    sizes=(2,)
)

@admin_router.message(Command("admin"))
async def add_produce(message: types.Message):
    await message.answer(text="Что хотите сделать?", reply_markup=ADMIN_KB)

@admin_router.message(F.text == "Ассортимент")
async def admin_features(message: types.Message, session: AsyncSession):
    categories = await orm_get_categories(session)
    btns = {category.name : f'category_{category.id}' for category in categories}
    await message.answer("Выберите категорию", reply_markup=get_callback_btns(btns=btns))


@admin_router.callback_query(F.data.startswith('category_'))
async def starring_at_product(callback: types.CallbackQuery, session: AsyncSession):
    category_id = callback.data.split('_')[-1]
    for product in await orm_get_products(session, int(category_id)):
        await callback.message.answer_photo(
            product.image,
            caption=f'<strong>{product.name}\
                    </strong>\n{product.description}\nСтоимость: {round(product.price, 2)}',
            reply_markup=get_callback_btns(
                btns={
                    "Удалить" : f"delete_{product.id}",
                    "Изменить" : f"change_{product.id}"
                },
                sizes=(2,)
            )
        )
    await callback.answer()
    await callback.message.answer("ОК, вот список товаров ⬆️")

@admin_router.callback_query(F.data.startswith("delete_"))
async def delete_product_callback(callback: types.CallbackQuery, session: AsyncSession):
    product_id = callback.data.split("_")[-1]
    await orm_delete_produce(session, int(product_id))

    await callback.answer("Товар удален")
    await callback.message.answer("Товар удален")


#############################   FSM для изменнеия баннеров   ####################################################

@admin_router.message(default_state, F.text == "Добавить/изменить баннер")
async def add_image2(message: types.Message, state: FSMContext, session: AsyncSession):
    pages_names = [page.name for page in await orm_get_info_pages(session=session)]
    await message.answer(f"Отправьте фото баннера. \nВ описании укажите для какой страницы:\
                         \n{', '.join(pages_names)}")
    await state.set_state(Addbanner.image)

@admin_router.message(Addbanner.image, F.photo)
async def add_banner(message: types.Message, state: FSMContext, session: AsyncSession):
    image_id = message.photo[-1].file_id
    for_page = message.caption.strip()
    pages_names = [page.name for page in await orm_get_info_pages(session)]

    if for_page not in pages_names:
        await message.answer(f"Введите нормальное название страницы, например:\
                             \n{','.join(pages_names)}")
        return
    await orm_change_banner_image(session, for_page, image_id)
    await message.answer("Баннер добавлен/изменен")
    await state.clear()

@admin_router.message(Addbanner.image)
async def add_banner2(message: types.Message, state: FSMContext):
    await message.answer("Отправьте фото баннера или отмена")

##############################   FSM для добавления/изменнения товаров админом   #########################################

@admin_router.callback_query(default_state, F.data.startswith("change_"))
async def change_product_callback(
    callback: types.CallbackQuery, state: FSMContext, session: AsyncSession
):
    product_id = callback.data.split("_")[-1]
    product_for_change = await orm_get_product(session, int(product_id))

    Addproduct.product_for_change = product_for_change

    await callback.answer()
    await callback.message.answer(
        "Введите название товара", reply_markup=types.ReplyKeyboardRemove()
    )

    await state.set_state(Addproduct.name)


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
    if Addproduct.product_for_change:
        Addproduct.product_for_change = None

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


@admin_router.message(Addproduct.name, F.text)
async def add_name(message: types.Message, state: FSMContext):
    if message.text == "." and Addproduct.product_for_change:
        await state.update_data(name=Addproduct.product_for_change.name)
    else:
        if 4 >= len(message.text) >= 150:
            await message.answer("Название товара не должно превышать 100 символов. \n Введите заново")
            return
    
        await state.update_data(name=message.text)
    await message.answer("Введите описание товара")
    await state.set_state(Addproduct.description)

@admin_router.message(Addproduct.name)
async def add_name2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, введите текст названия товара")



@admin_router.message(Addproduct.description, F.text)
async def add_description(message: types.Message, state: FSMContext, session: AsyncSession):
    if message.text == "." and Addproduct.product_for_change:
        await state.update_data(description=Addproduct.product_for_change.description)
    else:
        if 4 >= len(message.text):
            await message.answer(
                "Слишком короткое описание. \nВведите заново"
            )
            return
        await state.update_data(description=message.text)

    categories = await orm_get_categories(session)
    btns = {category.name : str(category.id) for category in categories} 
       
    await message.answer("Выберите категорию", reply_markup=get_callback_btns(btns=btns))
    await state.set_state(Addproduct.category)

@admin_router.message(Addproduct.description)
async def add_description2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, введите текст описания товара")


@admin_router.callback_query(Addproduct.category)
async def category_choice(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    if int(callback.data) in [category.id for category in await orm_get_categories(session)]:
        await callback.answer()
        await state.update_data(category=callback.data)
        await callback.message.answer('Теперь введите цену товара.')
        await state.set_state(Addproduct.price)
    else:
        await callback.message.answer('Выберите категорию из кнопок')
        await callback.answer()

@admin_router.callback_query(Addproduct.category)
async def category_choice2(message: types.Message, state: FSMContext):
    await message.answer("'Выберите категорию из кнопок")


@admin_router.message(Addproduct.price, F.text)
async def add_price(message: types.Message, state: FSMContext):
    if message.text == '.' and Addproduct.product_for_change:
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
    if message.text and message.text == "." and Addproduct.product_for_change:
        await state.update_data(image=Addproduct.product_for_change.image)
    elif message.photo:
        await state.update_data(image=message.photo[-1].file_id)
    else:
        await message.answer("Отправьте фото пищи")
        return
    
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