from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from internal.models.user import User


def generate_callbacks(prefix: str, n: int) -> [str]:
    callbacks = []
    for i in range(0, n):
        callbacks.append(f"{prefix}_{i}")
    return callbacks


def create_inline_keyboard(texts: [str], callback_data: [str]) -> InlineKeyboardMarkup:
    keyboard = []
    for i in range(0, len(texts)):
        keyboard.append([InlineKeyboardButton(text=texts[i], callback_data=callback_data[i])])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
