import logging

from fastapi import APIRouter, Header
from datetime import datetime

from uuid import uuid4

from internal.service.user import UserService
from internal.service.suggest import SuggestService
from internal.service.question import QuestionService
from internal.models.suggest import Suggest, SuggestRequest
from config.config import Config
from pkg.constants.constants import *
from pkg.utils.utils import *


class QuestionHTTPHandler:
    def __init__(self, cfg: Config, user_svc: UserService, suggest_svc: SuggestService, question_svc: QuestionService):
        self.cfg = cfg
        self.user_service = user_svc
        self.suggest_service = suggest_svc
        self.question_service = question_svc

        self.router = APIRouter(prefix='/question', tags=['question'])
        self.register_handlers()

    def register_handlers(self):
        @self.router.post("/suggest")
        async def suggest_handler(request: SuggestRequest, authorization: str = Header(None)):
            logging.info("suggest_handler: %s", request)
            logging.info("auth token: %s", authorization.split(" ")[1])

            user_telegram_id = DEFAULT_TELEGRAM_ID  # Значение по умолчанию
            try:
                user_telegram_id = verify_token(authorization.split(" ")[1], self.cfg.app.secret_key)
            except ValueError as e:
                logging.error("user with non verified token is suggested question")
            
            logging.info("telegram_id, that suggesting question: %s", user_telegram_id)

            suggest = Suggest(
                uuid=str(uuid4()),
                question=request.question,
                answers=request.answers,
                correct_id=request.correctAnswer,
                description=request.description,
                created_at=datetime.now(),
            )
            self.suggest_service.create_suggest(suggest, user_telegram_id)

            return {"message": "saved question"}
        
        @self.router.get("/suggests")
        async def get_suggests():
            suggests = self.suggest_service.get_all()
            if suggests is None:
                return {"message": "no questions"}
            
            return {"suggests": suggests}