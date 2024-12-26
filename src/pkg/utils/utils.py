import hashlib
import hmac
import base64

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from typing import List

from config.config import Application


def generate_callbacks(prefix: str, n: int) -> List[str]:
    callbacks = []
    for i in range(0, n):
        callbacks.append(f"{prefix}_{i}")
    return callbacks


def create_inline_keyboard(texts: List[str], callback_data: List[str]) -> InlineKeyboardMarkup:
    keyboard = []
    for i in range(0, len(texts)):
        keyboard.append([InlineKeyboardButton(text=texts[i], callback_data=callback_data[i])])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def add_reply_keyboard_button(kbd: ReplyKeyboardMarkup, txt: str) -> ReplyKeyboardMarkup:
    kbd.keyboard.append([KeyboardButton(text=txt)])


def generate_token(telegram_id: int, secret_key: str) -> str:
    signature = hmac.new(secret_key.encode(), str(telegram_id).encode(), hashlib.sha256).hexdigest()

    token = f"{telegram_id}.{signature}"
    print(f"token: {token}")
    print(f"encoded: {base64.urlsafe_b64encode(token.encode()).decode()}")
    return base64.urlsafe_b64encode(token.encode()).decode()


def verify_token(token, secret_key: str) -> int:
    try:
        decoded = base64.urlsafe_b64decode(token).decode()
        telegram_id, signature = decoded.split('.')
        expected_signature = hmac.new(secret_key.encode(), telegram_id.encode(), hashlib.sha256).hexdigest()
        if hmac.compare_digest(signature, expected_signature):
            return int(telegram_id)
    except Exception:
        raise ValueError("token is invlid")
