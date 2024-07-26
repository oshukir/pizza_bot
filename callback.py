from aiogram import F, Router, types
from aiogram.filters import Command
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

admin_router_cb = Router()
admin_router_cb.message.filter(ChatTypeFilter(['private']), IsAdmin())

@admin_router_cb.callback_query(F.data.startswith('delete_'))
async def delete_product(callback: types.CallbackQuery, session: AsyncSession):
    product_id = callback.data.split("_")[-1]
    await orm_delete_produce(session, int(product_id))

    await callback.answer()
    await callback.message.answer("Товар удален!")

@admin_router_cb.callback_query(default_state, F.data.startswith("change_"))
async def change_product_callback(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    product_id = callback.data.split("_")[-1]

    product_for_change = await orm_get_product(session, int(product_id))
    Addproduct.product_for_change = product_for_change

    await callback.answer()
    await callback.message.answer(
        text="Введите название товара", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(Addproduct.name)