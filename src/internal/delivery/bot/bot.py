from datetime import datetime
import logging

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.filters import Command
from aiogram import F

from src.internal.service.user import UserService
from src.internal.models.user import User
from .templates.messages import *
from .templates.keyboards import *
from src.pkg.constants.roles import *


class BotHandler:
    def __init__(self, bot: Bot, user_service: UserService):
        self.bot = bot
        self.user_service = user_service
        self.router = Router()

        self.register_handlers()

    def register_handlers(self):
        # /start
        @self.router.message(Command("start"))
        async def start_handler(message: Message):
            user = User(
                telegram_id=message.from_user.id,
                telegram_username=message.from_user.username,
                role=USER,
                created_at=datetime.now()
            )
            response = self.user_service.start_bot_using(user)

            if response.is_user_exists:
                await message.answer(START_HANDLER_RESPONSE_MSG, reply_markup=MAIN_MENU_KBD)
            else:
                # display buttons for determine level of knowledge
                await message.answer(KNOWLEDGE_LEVEL_DETERMINE_MSG, reply_markup=KNOWLEDGE_LEVEL_DETERMINE_KBD)

        # /help
        @self.router.message(Command("help"))
        @self.router.message(F.text.contains(bot_help))
        async def help_info(message: Message):
            await message.answer("not implemented")

        # /faq
        @self.router.message(Command("faq"))
        async def faq(message: Message):
            await message.answer("not implemented")

        # /feedback
        @self.router.message(Command("feedback"))
        async def feedback(message: Message):
            await message.answer("not implemented")

        # /lesson
        @self.router.message(Command("lesson"))
        @self.router.message(F.text.contains(start_lesson))
        async def get_lesson(message: Message):
            await message.answer("not implemented")

        # /profile
        @self.router.message(Command("profile"))
        @self.router.message(F.text.contains(profile))
        async def get_profile(message: Message):
            await message.answer("not implemented")

        # level_ selected
        @self.router.callback_query(F.data.startswith("level_"))
        async def handle_level_callback(callback: CallbackQuery):
            level = callback.data.split('_')[1]  # level_1 -> 1
            logging.info("user(%s) selected %s level", callback.from_user.username, level)

            user = User(
                telegram_id=callback.from_user.id,
                telegram_username=callback.from_user.username,
                level=level,
                updated_at=datetime.now()
            )
            self.user_service.update_user_info(user)

            response = LEVEL_ORIENTED_RESPONSE_MSG[level]

            await callback.message.edit_text(response)
            await callback.message.answer(FIRST_LESSON_TAKE_OFFER_MSG, reply_markup=MAIN_MENU_KBD)
            await callback.answer()
