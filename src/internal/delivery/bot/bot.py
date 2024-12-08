import logging

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command

from src.internal.service.user import UserService


class BotHandler:
    def __init__(self, bot: Bot, user_service: UserService):
        self.bot = bot
        self.user_service = user_service
        self.router = Router()

        self.register_handlers()

    def register_handlers(self):
        @self.router.message(Command("start"))
        async def start_handler(message: Message):
            logging.info("started user with id: %s", message.from_user.username)
            await message.answer(f"Привет! Твой ID: {message.from_user.id}")
