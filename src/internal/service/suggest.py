import logging
from uuid import uuid4
from datetime import datetime

from internal.storage.suggest import SuggestRepository
from internal.storage.user import UserRepository
from internal.models.suggest import Suggest, Check
from pkg.mappings.check_need import *
from pkg.constants.constants import *


class SuggestService:
    def __init__(self, suggest: SuggestRepository, user: UserRepository):
        self.suggest_repository = suggest
        self.user_repository = user

    def create_suggest(self, suggest: Suggest, telegram_id: int):
        user = self.user_repository.user_by_telegram_id(telegram_id)
        if user is None:
            logging.warning("no user with telegram_id: %s", telegram_id)
            return
        
        suggest.uuid = str(uuid4())
        suggest.created_at = datetime.now()
        suggest.set_proposing_user(user)
        suggest.check_need_count = CHECK_NEED_MAP.get(user.role)

        self.suggest_repository.create(suggest)

    def get_question_for_review(self) -> Suggest:
        return self.suggest_repository.get_for_review()
    
    def mark_as_correct(self, suggest_uuid: str, telegram_id: int):
        user = self.user_repository.user_by_telegram_id(telegram_id)
        if user is None:
            logging.warning("no user with telegram_id: %s", telegram_id)
            raise ValueError("no such user")

        suggest = self.suggest_repository.get_by_uuid(suggest_uuid)
        if suggest is None:
            logging.warning("no suggest with uuid: %s", suggest_uuid)
            raise ValueError("no such suggest")

        if suggest.marked_as_correct is None:
            suggest.marked_as_correct = []
        suggest.marked_as_correct.append(
            Check(
                telegram_id=user.telegram_id,
                telegram_username=user.telegram_username,
                checked_at=datetime.now(),
            )
        )

        self.suggest_repository.update(suggest)

    def mark_as_bad(self, suggest_uuid: str, comment: str, telegram_id: int):
        user = self.user_repository.user_by_telegram_id(telegram_id)
        if user is None:
            logging.warning("no user with telegram_id: %s", telegram_id)
            raise ValueError("no such user")
        
        suggest = self.suggest_repository.get_by_uuid(suggest_uuid)
        if suggest is None:
            logging.warning("no suggest with uuid: %s", suggest_uuid)
            raise ValueError("no such suggest")

        if suggest.marked_as_erroneous is None:
            suggest.marked_as_erroneous = []
        suggest.marked_as_erroneous.append(
            Check(
                telegram_id=user.telegram_id,
                telegram_username=user.telegram_username,
                comment=comment,
                checked_at=datetime.now(),
            )
        )

        self.suggest_repository.update(suggest)

    def mark_as_improve(self, suggest_uuid: str, comment: str, telegram_id: int):
        user = self.user_repository.user_by_telegram_id(telegram_id)
        if user is None:
            logging.warning("no user with telegram_id: %s", telegram_id)
            raise ValueError("no such user")
        
        suggest = self.suggest_repository.get_by_uuid(suggest_uuid)
        if suggest is None:
            logging.warning("no suggest with uuid: %s", suggest_uuid)
            raise ValueError("no such suggest")

        if suggest.marked_as_improve is None:
            suggest.marked_as_improve = []
        suggest.marked_as_improve.append(
            Check(
                telegram_id=user.telegram_id,
                telegram_username=user.telegram_username,
                comment=comment,
                checked_at=datetime.now(),
            )
        )

        self.suggest_repository.update(suggest)
