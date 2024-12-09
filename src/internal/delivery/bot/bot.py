import logging

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram import F

from src.internal.service.user import UserService
from src.internal.models.user import StartBotUsingRequest
from .templates import *


class BotHandler:
    def __init__(self, bot: Bot, user_service: UserService):
        self.bot = bot
        self.user_service = user_service
        self.router = Router()

        self.register_handlers()

    def register_handlers(self):
        @self.router.message(Command("start"))
        async def start_handler(message: Message):
            request = StartBotUsingRequest(message)
            response = self.user_service.start_bot_using(request)

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

        @self.router.callback_query(F.text.startswith("level_"))
        async def handle_level_callback(callback: CallbackQuery):
            level = callback.data.split('-')[1]
            logging.info("level: %s", level)
            await callback.message.answer("Отлично, давай начнем изучение")
            await callback.answer()
