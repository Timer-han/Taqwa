import logging

from fastapi import APIRouter, Header, Request, HTTPException
from datetime import datetime

from uuid import uuid4, UUID

from internal.service.user import UserService
from internal.service.suggest import SuggestService
from internal.service.question import QuestionService
from internal.models.suggest import Suggest, SuggestRequest, SuggestReview
from config.config import Config
from pkg.constants.constants import *
from pkg.constants.review import *
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
        async def suggest_handler(request: Request, body: SuggestRequest, authorization: str = Header(None)):
            user_telegram_id = int(getattr(request.state, "telegram_id"))
            if not user_telegram_id:
                return {"error": "Unauthorized access"}

            suggest = Suggest(
                uuid=str(uuid4()),
                question=body.question,
                answers=body.answers,
                correct_id=body.correctAnswer,
                description=body.description,
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
        
        @self.router.get("/review-suggests")
        async def get_review_suggests(request: Request):
            user_telegram_id = int(getattr(request.state, "telegram_id"))
            if not user_telegram_id:
                return {"error": "Unauthorized access"}
            
            suggests = self.suggest_service.get_all_for_review(int(user_telegram_id))
            if suggests is None:
                return {"message": "no questions"}
            
            return {"suggests": suggests}
        
        @self.router.get("/suggest")
        async def get_suggest_by_uuid(request: Request):
            suggest_uuid = request.query_params.get("uuid")
            logging.info("getting suggest by uuid: %s", suggest_uuid)

            if not suggest_uuid:
                raise HTTPException(status_code=400, detail="UUID параметр обязателен")
            
            try:
                uuid_obj = UUID(suggest_uuid)
            except ValueError:
                raise HTTPException(status_code=400, detail="Некорректный UUID")
            
            suggest = self.suggest_service.get_by_uuid(suggest_uuid)
            if not suggest:
                raise HTTPException(status_code=404, detail="Вопрос не найден")
            
            return {"suggest": suggest}
    
        @self.router.post("/suggest/review")
        async def review(request: Request, body: SuggestReview):
            user_telegram_id = int(getattr(request.state, "telegram_id"))
            if not user_telegram_id:
                return {"error": "Unauthorized access"}

            suggest_uuid = request.query_params.get("uuid")
            logging.info("suggest_review_handler: %s", body)
            logging.info("suggest_uuid: %s", suggest_uuid)

            if body.type == GOOD_BUTTON:
                self.suggest_service.mark_as_correct(suggest_uuid, user_telegram_id)
            elif body.type == BAD_BUTTON:
                self.suggest_service.mark_as_bad(suggest_uuid, body.comment, user_telegram_id)
            elif body.type == IMPROVE_BUTTON:
                self.suggest_service.mark_as_improve(suggest_uuid, body.comment, user_telegram_id)
