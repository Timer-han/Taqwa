import uuid

from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class StartBotUsingResponse:
    is_user_exists: bool

    def __init__(self, is_exists):
        self.is_user_exists = is_exists


class User(BaseModel):
    uuid: Optional[str] = None
    telegram_id: Optional[int] = None
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