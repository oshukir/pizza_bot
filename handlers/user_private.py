from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message
)
from filters.chat_types import ChatTypeFilter
from keyboards.reply import get_keyboard

from database.orm_query import (
    orm_get_products
)
from database.engine import session_maker
from sqlalchemy.ext.asyncio import AsyncSession

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter('private'))

@user_private_router.message(Command('start'))
async def start_cmd(message: Message):
    await message.answer("Привет, я виртуальный помощник",
                         reply_markup=get_keyboard(
                             "Меню",
                             "О магазине",
                             "Варианты оплаты",
                             "Варианты доставки",
                             placeholder="Что вас интересует",
                             sizes=(2,2)
                         ))

@user_private_router.message(Command("menu"))
@user_private_router.message(F.text.lower() == "меню")
async def start_cmd(message: Message, session: AsyncSession):
    for product in await orm_get_products(session=session):
        await message.answer_photo(
            product.image,
            caption=f"{product.name}\n{product.description}\nСтоимость:{round(product.price, 2)} тг"
        )
    await message.answer("Вот меню ⬆️")

@user_private_router.message(Command("about"))
@user_private_router.message(F.text.lower() == "о магазине")
async def start_cmd(message: Message):
    await message.answer("О нас")

@user_private_router.message(Command("payment"))
@user_private_router.message(F.text.lower() == "варианты оплаты")
async def start_cmd(message: Message):
    await message.answer("Варианты оплаты:")

@user_private_router.message(Command("shipping"))
@user_private_router.message(F.text.lower() == "варианты доставки")
async def start_cmd(message: Message):
    await message.answer("Варианты доставки")

@user_private_router.message(F.contact)
async def get_contact(message: Message):
    await message.answer(f"номер получен")

@user_private_router.message(F.location)
async def get_contact(message: Message):
    await message.answer(f"локация получена")

