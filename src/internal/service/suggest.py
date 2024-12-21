import logging

from internal.storage.suggest import SuggestRepository
from internal.storage.user import UserRepository
from internal.models.suggest import Suggest
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

        suggest.set_proposing_user(user)
        suggest.check_need_count = CHECK_NEED_MAP.get(user.role)

        self.suggest_repository.create(suggest)

    # def set_correct_answer(self, answer_id: int):