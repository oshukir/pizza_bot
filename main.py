import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import (
    BotCommand,
    BotCommandScopeAllPrivateChats
)
from config_reader import config
# from common.bot_cmds_list import private

from handlers.user_private import user_private_router
from handlers.user_group import user_group_router
from handlers.admin_private import admin_router
from callback import admin_router_cb

from database.engine import create_db, drop_db
from database.engine import session_maker

from middlewares.db import DataBaseSession

async def on_startup(bot):

    # await drop_db()
    await create_db()

async def on_shutdown(bot):
    print("bot is off")

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp = Dispatcher()
    bot = Bot(
        config.bot_token.get_secret_value(),
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    dp.include_routers(
        user_private_router,
        user_group_router,
        admin_router,
        admin_router_cb,
    )

    # await bot.delete_my_commands()
    # await bot.set_my_commands(commands=private, scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=["message", "inline_query", "my_chat_member", "chat_member", "callback_query"])
if __name__ == "__main__":
    asyncio.run(main())