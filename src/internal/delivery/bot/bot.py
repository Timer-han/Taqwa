from datetime import datetime
import logging

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram import F

from src.internal.service.user import UserService
from src.internal.models.user import User
from .templates import *
from src.pkg.constants.roles import *


class BotHandler:
    def __init__(self, bot: Bot, user_service: UserService):
        self.bot = bot
        self.user_service = user_service
        self.router = Router()

        self.register_handlers()

    def register_handlers(self):
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
                await message.answer(START_HANDLER_RESPONSE)
            else:
                new_user_kbd = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="1", callback_data="level_1")],
                    [InlineKeyboardButton(text="2", callback_data="level_2")],
                    [InlineKeyboardButton(text="3", callback_data="level_3")],
                    [InlineKeyboardButton(text="4", callback_data="level_4")],
                    [InlineKeyboardButton(text="5", callback_data="level_5")],
                ])
                await message.answer(NEW_USER_RESPONSE, reply_markup=new_user_kbd)

        @self.router.callback_query(F.data.startswith("level_"))
        async def handle_level_callback(callback: CallbackQuery):
            level = callback.data.split('_')[1]
            logging.info("user(%s) selected %s level", callback.from_user.username, level)

            user = User(
                telegram_id=callback.from_user.id,
                telegram_username=callback.from_user.username,
                level=level,
                updated_at=datetime.now()
            )
            self.user_service.update_user_info(user)

            response = LEVEL_ORIENTED_RESPONSE[level]

            await callback.message.answer(response)
            await callback.message.answer(FIRST_LESSON_TAKE_OFFER)
            await callback.answer()
