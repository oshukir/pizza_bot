from aiogram import types, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message
)

user_private_router = Router()

@user_private_router.message(CommandStart)
async def start_cmd(message: Message):
    await message.answer("Привет, я виртуальный помощник")

@user_private_router.message(Command("menu"))
async def start_cmd(message: Message):
    await message.answer("Вот меню")

@user_private_router.message(Command("about"))
async def start_cmd(message: Message):
    await message.answer("О нас")

@user_private_router.message(Command("payment"))
async def start_cmd(message: Message):
    await message.answer("Врианты оплаты:")

@user_private_router.message(Command("shipping"))
async def start_cmd(message: Message):
    await message.answer("Варианты доставки")

