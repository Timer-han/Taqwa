from datetime import datetime
from aiogram.types import Message
from dataclasses import asdict
from pydantic import BaseModel
from typing import Optional, List

from src.pkg.constants.roles import *


class StartBotUsingRequest:
    telegram_id: int
    username: str

    def __init__(self, message: Message):
        self.telegram_id = message.from_user.id
        self.username = message.from_user.username

    def __str__(self):
        return (f"StartBotUsingRequest("
                f"id={self.telegram_id}, "
                f"username={self.username}")


class StartBotUsingResponse:
    is_user_exists: bool

    def __init__(self, is_exists):
        self.is_user_exists = is_exists


class User(BaseModel):
    telegram_id: int
    telegram_username: Optional[str] = None
    strike: Optional[int] = None
    role: Optional[str] = "user"
    level: Optional[int] = None
    last_chapter_passed: Optional[int] = None
    last_lesson_passed: Optional[int] = None
    followings: Optional[List[int]] = None
    followers: Optional[List[int]] = None
    added_questions_count: Optional[int] = None
    verified_questions_count: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
