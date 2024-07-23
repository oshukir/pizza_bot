import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import BotCommand
from config_reader import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler



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


    
    
    await dp.start_polling(bot, allowed_updates=["message", "inline_query", "my_chat_member", "chat_member", "callback_query"])
if __name__ == "__main__":
    asyncio.run(main())