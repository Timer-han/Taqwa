import asyncio
import logging
import time

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from internal.storage.user import UserRepository
from internal.service.user import UserService
from internal.delivery.bot.bot import BotHandler
from config.config import load_config


async def main():
    env = load_config()
    logging.info("config loaded successfully")

    user_repository = UserRepository() # database init

    user_service = UserService(user_repository) # business logic init

    bot = Bot(token=env.bot.api_token) # bot init
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
        level=logging.DEBUG,
    )
    logging.info("starting app")
    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            print("Перезапуск через 5 секунд...")
            time.sleep(5)
