import logging

from src.internal.storage.user import UserRepository
from src.internal.models.user import User, StartBotUsingRequest, StartBotUsingResponse


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def start_bot_using(self, request: StartBotUsingRequest) -> StartBotUsingResponse:
        logging.info("some request with values: %s", request)

        user = self.repository.user_by_telegram_id(request.telegram_id)
        if user is not None:
            return StartBotUsingResponse(True)

        user = User(
            telegram_id=request.telegram_id,
            telegram_username=request.username,
        )
        self.repository.create_user(user)

        return StartBotUsingResponse(False)