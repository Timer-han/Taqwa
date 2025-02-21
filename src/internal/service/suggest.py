import logging
from uuid import uuid4
from datetime import datetime
from typing import List

from internal.storage.suggest import SuggestRepository
from internal.storage.user import UserRepository
from internal.models.suggest import Suggest, Check, ReviewedCountResponse
from internal.models.user import User
from pkg.mappings.check_need import *
from pkg.constants.constants import *
from pkg.errors.errors import *

class SuggestService:
    def __init__(self, suggest: SuggestRepository, user: UserRepository):
        self.suggest_repository = suggest
        self.user_repository = user

    def create_suggest(self, suggest: Suggest, telegram_id: int):
        user = self.user_repository.user_by_telegram_id(telegram_id)
        if user is None or user.role == NOBODY:
            logging.warning("no user with telegram_id: %s", telegram_id)
            return
        
        suggest.uuid = str(uuid4())
        suggest.created_at = datetime.now()
        suggest.set_proposing_user(user)
        suggest.check_need_count = CHECK_NEED_MAP.get(user.role)

        self.suggest_repository.create(suggest)

    def get_all(self) -> List[Suggest]:
        return self.suggest_repository.get_all()
    
    def get_all_for_review(self, telegram_id: int) -> List[Suggest]:
        user = self.user_repository.user_by_telegram_id(telegram_id)
        if user is None:
            raise UserNotFoundError("no user with such telegram id")
        
        if user.role not in [ADMIN, SUPER_ADMIN, OWNER]:
            raise PermissionDeniedError("this user doesn't have permission for handler")

        suggests = self.suggest_repository.get_all()
        if suggests is None:
            return None
        
        response = []
        for suggest in suggests:
            in_marked_as_correct = any(check.telegram_id == telegram_id for check in (suggest.marked_as_correct or []))
            in_marked_as_erroneous = any(check.telegram_id == telegram_id for check in (suggest.marked_as_erroneous or []))
            in_marked_as_improve = any(check.telegram_id == telegram_id for check in (suggest.marked_as_improve or []))
            
            if not (in_marked_as_correct or in_marked_as_erroneous or in_marked_as_improve):
                response.append(suggest)
        
        return response
        
    
    def get_by_uuid(self, uuid: str) -> Suggest:
        return self.suggest_repository.get_by_uuid(uuid)

    def get_question_for_review(self, user: User) -> Suggest:
        return self.suggest_repository.get_for_review(user)
    
    def mark_as_correct(self, suggest_uuid: str, telegram_id: int):
        user = self.user_repository.user_by_telegram_id(telegram_id)
        if user is None:
            logging.warning("no user with telegram_id: %s", telegram_id)
            raise ValueError("no such user")
        
        if user.role not in [ADMIN, SUPER_ADMIN, OWNER]:
            raise ValueError("this user doesn't have permission for handler")

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

    def mark_as_bad(self, suggest_uuid: str, telegram_id: int):
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

    def get_reviewed_count(self, telegram_id: int) -> ReviewedCountResponse:        
        reviewed_count = self.suggest_repository.get_reviewed_count(telegram_id)
        total_count = self.suggest_repository.get_total_count()

        return ReviewedCountResponse(
            reviewed_count=reviewed_count,
            total_count=total_count
        )