import asyncio
import logging
import time

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from internal.storage.mongo import MongoDatabase
from internal.storage.user import UserRepository
from internal.service.user import UserService
from internal.delivery.bot.bot import BotHandler
from config.config import load_config


async def main():
    cfg = load_config()
    logging.info("config loaded successfully")

    mongo_db = MongoDatabase(cfg.database)

    # database init
    user_repository = UserRepository(mongo_db)

    # business logic init
    user_service = UserService(user_repository)

    # bot init
    bot = Bot(token=cfg.bot.api_token)
    dp = Dispatcher(storage=MemoryStorage())

    bot_handlers = BotHandler(bot, user_service)
    dp.include_router(bot_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )
    logging.info("starting app")
    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            logging.error("Error occurred: %s", e)
            logging.info("Restarting in 5 seconds")
            time.sleep(5)
