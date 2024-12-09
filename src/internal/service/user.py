from src.internal.storage.user import UserRepository
from src.internal.models.user import User, StartBotUsingResponse


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def start_bot_using(self, user: User) -> StartBotUsingResponse:
        db_user = self.repository.user_by_telegram_id(user.telegram_id)
        if db_user is not None:
            return StartBotUsingResponse(True)

        self.repository.create_user(user)

        return StartBotUsingResponse(False)

    def update_user_info(self, request: User):
        self.repository.update_user(request)
