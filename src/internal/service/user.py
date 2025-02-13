from uuid import uuid4
from datetime import datetime

from internal.storage.user import UserRepository
from internal.models.user import *
from pkg.constants.roles import USER, ADMIN, NOBODY


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    # start_bot_using saving user and returns him and is he existed before
    def start_bot_using(self, user: User):
        db_user = self.repository.user_by_telegram_id(user.telegram_id)
        if not (db_user is None or db_user.role == NOBODY):
            return db_user, True

        user.uuid = str(uuid4())
        # TODO: change to USER
        user.role = ADMIN
        user.created_at = datetime.now()

        self.repository.create_user(user)

        return user, False

    def set_knowledge_level(self, telegram_id: int, level: int):
        user = self.repository.user_by_telegram_id(telegram_id)
        user.level = level
        user.updated_at = datetime.now()

        self.repository.update_user(user)

    def get_by_telegram_id(self, telegram_id: int) -> User:
        return self.repository.user_by_telegram_id(telegram_id)
    