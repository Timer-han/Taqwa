import asyncio
import logging
import time
import uvicorn
from fastapi import FastAPI

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi.middleware.cors import CORSMiddleware

from src.internal.storage.mongo import MongoDatabase
from src.internal.storage.user import UserRepository
from src.internal.storage.suggest import SuggestRepository
from src.internal.storage.question import QuestionRepository
from src.internal.service.user import UserService
from src.internal.service.suggest import SuggestService
from src.internal.service.question import QuestionService
from src.internal.delivery.bot.bot import BotHandler
from src.internal.delivery.http.question import QuestionHTTPHandler
from src.config.config import load_config
from src.pkg.logger.logger import *

cfg = load_config()
app = FastAPI()
origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
    question_handler = QuestionHTTPHandler(user_service, suggest_service, question_service)

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

    bot_handlers = BotHandler(bot, user_service, suggest_service, question_service)
    dp.include_router(bot_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def start_fastapi():
    config = uvicorn.Config("src.main:app", host=cfg.app.host, port=int(cfg.app.port), reload=True)
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


@app.get("/health")
async def healthcheck():
    return {"message": "success"}