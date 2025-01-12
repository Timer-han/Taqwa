import asyncio
import logging
import time
import uvicorn
from fastapi import FastAPI

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi.middleware.cors import CORSMiddleware

from internal.storage.mongo import MongoDatabase
from internal.storage.user import UserRepository
from internal.storage.suggest import SuggestRepository
from internal.storage.question import QuestionRepository
from internal.service.user import UserService
from internal.service.suggest import SuggestService
from internal.service.question import QuestionService
from internal.delivery.bot.bot import BotHandler
from internal.delivery.http.suggest import SuggestHTTPHandler
from internal.middleware.auth import AuthMiddleware
from config.config import load_config
from pkg.logger.logger import *

cfg = load_config()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuthMiddleware, secret_key=cfg.app.secret_key)
logging.basicConfig(
    format=LOG_FORMAT,
    datefmt=LOG_DATE_FORMAT,
    level=LOG_LEVEL,
)


def setup_fastapi_routes():
    mongo_db = MongoDatabase(cfg.database)

    # Repositories
    user_repository = UserRepository(mongo_db)
    suggest_repository = SuggestRepository(mongo_db)
    question_repository = QuestionRepository(mongo_db)

    # Services
    user_service = UserService(user_repository)
    suggest_service = SuggestService(suggest_repository, user_repository)
    question_service = QuestionService(question_repository)

    # HTTP Handlers
    question_handler = SuggestHTTPHandler(cfg, user_service, suggest_service, question_service)

    app.include_router(question_handler.router)


setup_fastapi_routes()


async def start_bot():
    mongo_db = MongoDatabase(cfg.database)

    # database init
    user_repository = UserRepository(mongo_db)
    suggest_repository = SuggestRepository(mongo_db)
    question_repository = QuestionRepository(mongo_db)

    # business logic init
    user_service = UserService(user_repository)
    suggest_service = SuggestService(suggest_repository, user_repository)
    question_service = QuestionService(question_repository)

    # bot init
    bot = Bot(token=cfg.bot.api_token)
    dp = Dispatcher(storage=MemoryStorage())

    bot_handlers = BotHandler(cfg, bot, user_service, suggest_service, question_service)
    dp.include_router(bot_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def start_fastapi():
    config = uvicorn.Config("main:app", host=cfg.app.host, port=int(cfg.app.port), reload=True)
    server = uvicorn.Server(config)
    set_uvicorn_logger()
    await server.serve()


async def main():
    bot_task = asyncio.create_task(start_bot())
    fastapi_task = asyncio.create_task(start_fastapi())

    await asyncio.gather(bot_task, fastapi_task)


if __name__ == "__main__":
    logging.info("starting app")
    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            logging.error("Error occurred: %s", e)
            logging.info("Restarting in 5 seconds")
            time.sleep(5)


@app.get("/health/{id}")
async def healthcheck(id: int):
    return {"message": f"success with id: {id}"}