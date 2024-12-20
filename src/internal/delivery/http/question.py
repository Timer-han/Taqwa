import logging

from fastapi import APIRouter
from datetime import datetime

from uuid import uuid4

from internal.service.user import UserService
from internal.service.suggest import SuggestService
from internal.service.question import QuestionService
from internal.models.suggest import Suggest, SuggestRequest
from pkg.constants.constants import *


class QuestionHTTPHandler:
    def __init__(self, user_svc: UserService, suggest_svc: SuggestService, question_svc: QuestionService):
        self.user_service = user_svc
        self.suggest_service = suggest_svc
        self.question_service = question_svc

        self.router = APIRouter(prefix='/question', tags=['question'])
        self.register_handlers()

    def register_handlers(self):
        @self.router.post("/suggest")
        async def suggest_handler(request: SuggestRequest):
            logging.info("suggest_handler: %s", request)
            suggest = Suggest(
                uuid=str(uuid4()),
                question=request.question,
                answers=request.answers,
                correct_id=request.correctAnswer,
                created_at=datetime.now(),
            )
            self.suggest_service.create_suggest(suggest, DEFAULT_TELEGRAM_ID)

            return {"message": "saved question"}