import logging

from fastapi import APIRouter, Header, Request, HTTPException
from fastapi.responses import JSONResponse
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
from pkg.errors.errors import *


class SuggestHTTPHandler:
    def __init__(self, cfg: Config, user_svc: UserService, suggest_svc: SuggestService, question_svc: QuestionService):
        self.cfg = cfg
        self.user_service = user_svc
        self.suggest_service = suggest_svc
        self.question_service = question_svc

        self.router = APIRouter(prefix='/suggest', tags=['suggest'])
        self.register_handlers()

    def register_handlers(self):
        @self.router.post("/")
        async def suggest_handler(request: Request, body: SuggestRequest, authorization: str = Header(None)):
            user_telegram_id = int(getattr(request.state, "telegram_id"))
            logging.info("%s: suggesting question", user_telegram_id)
            if not user_telegram_id:
                return {"error": "Unauthorized access"}

            suggest = Suggest(
                uuid=str(uuid4()),
                question=body.question,
                answers=body.answers,
                correct_id=body.correctAnswer,
                description=body.description,
                difficulty=body.difficulty,
                created_at=datetime.now(),
            )
            self.suggest_service.create_suggest(suggest, user_telegram_id)

            return {"message": "saved question"}
        
        @self.router.get("/all")
        async def get_suggests():
            suggests = self.suggest_service.get_all()
            if suggests is None:
                return {"message": "no questions"}
            
            return {"suggests": suggests}
        
        @self.router.get("/review")
        async def get_review_suggests(request: Request):
            user_telegram_id = int(getattr(request.state, "telegram_id"))
            logging.info("%s: getting question for review", user_telegram_id)
            if not user_telegram_id:
                return {"status": "error", "message": "Пользователь не авторизован, нужно перейти по ссылке из бота"}
            
            try:
                suggests = self.suggest_service.get_all_for_review(int(user_telegram_id))
            except UserNotFoundError:
                return JSONResponse(
                    status_code=404, content={"status": "error", "message": "Пользователь не найден"}
                )
            except PermissionDeniedError:
                return JSONResponse(
                    status_code=403, content={"status": "error", "message": "У вас нет прав для выполнения этого действия"}
                )
            except Exception as e:
                logging.error("error occured in get_review_suggests: %s", e)
                return JSONResponse(
                    status_code=500, content={"status": "error", "message": "Ошибка сервера, пожалуйста обратись в поддержку"}
                )
            
            return {"length": len(suggests), "suggests": suggests}
        
        @self.router.get("/")
        async def get_suggest_by_uuid(request: Request):
            suggest_uuid = request.query_params.get("uuid")

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
    
        @self.router.post("/make-review")
        async def review(request: Request, body: SuggestReview):
            user_telegram_id = int(getattr(request.state, "telegram_id"))
            logging.info("%s: reviewing question with answer - %s", user_telegram_id, body.type)
            if not user_telegram_id:
                return {"error": "Unauthorized access"}

            suggest_uuid = request.query_params.get("uuid")

            try:
                if body.type == GOOD_BUTTON:
                    self.suggest_service.mark_as_correct(suggest_uuid, user_telegram_id)
                elif body.type == BAD_BUTTON:
                    self.suggest_service.mark_as_bad(suggest_uuid, body.comment, user_telegram_id)
                elif body.type == IMPROVE_BUTTON:
                    self.suggest_service.mark_as_improve(suggest_uuid, body.comment, user_telegram_id)
            except ValueError as e:
                return JSONResponse(
                    status_code=500, content={"error": e}
                )