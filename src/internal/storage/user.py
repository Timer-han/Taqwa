from .mongo import MongoDatabase
from typing import Optional
import logging
from dataclasses import asdict

from src.internal.models.user import User
from src.pkg.constants.roles import *

telegram_id_column = "telegram_id"


class UserRepository:
    def __init__(self, db: MongoDatabase):
        self.collection = db.get_collection("users")

    def user_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        document = self.collection.find_one({telegram_id_column: telegram_id})
        if document is None:
            return None

        user_data = {field: document.get(field) for field in User.__annotations__.keys()}
        logging.info("getting_user: %s", user_data)
        return User(**user_data)

    def create_user(self, user: User):
        logging.info("creating_user: %s", user.dict(exclude_none=True))
        self.collection.insert_one(user.dict(exclude_none=True))

    def update_user(self, user: User):
        logging.info("updating_user: %s", user.dict(exclude_none=True))
        document = self.collection.find_one_and_update(
            {telegram_id_column: user.telegram_id},
            {"$set": user.dict(exclude_none=True)},
            return_document=True,
        )

        user_data = {field: document.get(field) for field in User.__annotations__.keys()}
        logging.info("updated_user: %s", user_data)
        return User(**user_data)
