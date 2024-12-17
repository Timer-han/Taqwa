from src.internal.storage.suggest import SuggestRepository
from src.internal.storage.user import UserRepository
from src.internal.models.suggest import Suggest
from src.pkg.mappings.check_need import *


class SuggestService:
    def __init__(self, suggest: SuggestRepository, user: UserRepository):
        self.suggest_repository = suggest
        self.user_repository = user

    def create_suggest(self, suggest: Suggest, telegram_id: int):
        user = self.user_repository.user_by_telegram_id(telegram_id)

        suggest.set_proposing_user(user)
        suggest.check_need_count = CHECK_NEED_MAP.get(user.role)

        self.suggest_repository.create(suggest)

    # def set_correct_answer(self, answer_id: int):