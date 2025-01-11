from datetime import datetime
import logging

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.filters import Command
from aiogram import F
from aiogram.fsm.context import FSMContext

from internal.service.user import UserService
from internal.service.suggest import SuggestService
from internal.service.question import QuestionService
from internal.models.user import User
from internal.models.suggest import Suggest
from .templates.messages import *
from .templates.keyboards import *
from .templates.states import *
from pkg.constants.roles import *
from pkg.utils.utils import *
from config.config import Config


class BotHandler:
    def __init__(self, cfg: Config, bot: Bot, user_svc: UserService, suggest_svc: SuggestService, question_svc: QuestionService):
        self.cfg = cfg
        self.bot = bot
        self.user_service = user_svc
        self.suggest_service = suggest_svc
        self.question_service = question_svc

        self.router = Router()
        self.register_handlers()

    def register_handlers(self):
        # /start
        @self.router.message(Command("start"))
        async def start_handler(message: Message):
            logging.info("starting")
            user = User(
                telegram_id=message.from_user.id,
                telegram_username=message.from_user.username,
            )
            response, is_existed_before = self.user_service.start_bot_using(user)
            if is_existed_before:
                await message.answer(START_HANDLER_RESPONSE_MSG, reply_markup=self.set_main_menu_kbd(message.from_user.id))
            else:
                # display buttons for determine level of knowledge
                await message.answer(KNOWLEDGE_LEVEL_DETERMINE_MSG, reply_markup=KNOWLEDGE_LEVEL_DETERMINE_KBD)

        # /help || bot_help button
        @self.router.message(Command("help"))
        @self.router.message(F.text.contains(bot_help))
        async def help_info(message: Message):
            await message.answer("not implemented")

        # /faq
        @self.router.message(Command("faq"))
        async def faq(message: Message):
            await message.answer("not implemented")

        # /feedback
        @self.router.message(Command("feedback"))
        async def feedback(message: Message):
            await message.answer("not implemented")

        # /lesson || start_lesson button
        @self.router.message(Command("lesson"))
        @self.router.message(F.text.contains(start_lesson))
        async def get_lesson(message: Message):
            await message.answer("not implemented")

        # /profile || profile button
        @self.router.message(Command("profile"))
        @self.router.message(F.text.contains(profile))
        async def get_profile(message: Message):
            token = generate_token(message.from_user.id, self.cfg.app.secret_key)
            url = self.cfg.other.dns_name + "?token=" + token

            await message.answer(PROFILE_MSG+url, reply_markup=self.set_main_menu_kbd(message.from_user.id))

        # /suggest || question_suggest button
        @self.router.message(Command("suggest"))
        @self.router.message(F.text.contains(question_suggest))
        async def suggest_question(message: Message, state: FSMContext):
            await message.answer(QUESTION_SUGGEST_MSG, parse_mode="HTML", reply_markup=CANCEL_KBD)
            await state.set_state(SuggestQuestionState.waiting_for_question)

        @self.router.message(SuggestQuestionState.waiting_for_question)
        async def receive_question(message: Message, state: FSMContext):
            if message.text == cancel:
                logging.info("sent cancel question message")
                await state.clear()
                await message.answer(QUESTION_CANCEL_MSG, reply_markup=self.set_main_menu_kbd(message.from_user.id))
                return

            logging.info("receive question: %s", message.text)
            await state.update_data(question=message.text)
            await message.answer(QUESTION_RECEIVE_MSG, parse_mode='HTML')
            await state.set_state(SuggestQuestionState.waiting_for_answers)

        @self.router.message(SuggestQuestionState.waiting_for_answers)
        async def receive_answers(message: Message, state: FSMContext):
            if message.text == cancel:
                logging.info("sent cancel question message")
                await state.clear()
                await message.answer(QUESTION_CANCEL_MSG, reply_markup=self.set_main_menu_kbd(message.from_user.id))
                return

            logging.info("receive answers: %s", message.text)
            answers = [answer.strip() for answer in message.text.split("\n")]
            if len(answers) < 2 or len(answers) > 5:
                await message.answer("Пожалуйста, введите от 2 до 5 вариантов ответа")
                return

            txt = CORRECT_ANSWERS_RECEIVE_MSG
            callbacks = generate_callbacks("suggest", len(answers))
            kbd = create_inline_keyboard(answers, callbacks)

            await state.update_data(answers=answers)
            await message.answer(txt, reply_markup=kbd)

        # suggest_ selected
        @self.router.callback_query(F.data.startswith("suggest_"))
        async def handle_suggested_correct_answer(callback: CallbackQuery, state: FSMContext):
            correct_answer = callback.data.split('_')[1]  # suggest_1 -> 1
            logging.info("correct answer %s chosen", correct_answer)

            if not correct_answer.isnumeric():
                await callback.answer("Что-то тут не так, если не получается решить проблему, напиши нам)")
                return
            
            await state.update_data(correct_id=int(correct_answer))
            await callback.message.edit_text(DESCRIPTION_NEED_MSG, parse_mode='HTML')
            await state.set_state(SuggestQuestionState.waiting_for_description)

            # question = await state.get_value("question")
            # answers = await state.get_value("answers")
            # suggest = Suggest(
            #     question=question,
            #     answers=answers,
            #     correct_id=int(correct_answer),
            # )
            # await state.clear()
            
            # self.suggest_service.create_suggest(suggest, callback.from_user.id)

            # await callback.message.edit_text(QUESTION_SUGGEST_GRATITUDE_MSG)
            # await callback.answer(reply_markup=self.set_main_menu_kbd(callback.from_user.id))
        
        @self.router.message(SuggestQuestionState.waiting_for_description)
        async def receive_answers(message: Message, state: FSMContext):
            if message.text == cancel:
                logging.info("sent cancel question message")
                await state.clear()
                await message.answer(QUESTION_CANCEL_MSG, reply_markup=self.set_main_menu_kbd(message.from_user.id))
                return
            
            logging.info("receive description: %s", message.text)
            question = await state.get_value("question")
            answers = await state.get_value("answers")
            correct_id = await state.get_value("correct_id")
            suggest = Suggest(
                question=question,
                answers=answers,
                correct_id=correct_id,
                description=message.text,
            )
            
            self.suggest_service.create_suggest(suggest, message.from_user.id)

            await state.clear()
            await message.answer(QUESTION_SUGGEST_GRATITUDE_MSG, reply_markup=self.set_main_menu_kbd(message.from_user.id))
        
        # /review || review_question button
        @self.router.message(Command("review"))
        @self.router.message(F.text.contains(question_review))
        async def handler_question_review(message: Message, state: FSMContext):

            # admin check
            if self.user_service.get_by_telegram_id(message.from_user.id).role != ADMIN:
                await message.answer(GET_ADMIN_RIGHTS, reply_markup=self.set_main_menu_kbd(message.from_user.id))
                return

            user = self.user_service.get_by_telegram_id(message.from_user.id)
            suggest = self.suggest_service.get_question_for_review(user)
            if suggest is None:
                await message.answer(NO_QUESTIONS_FOR_REVIEW_MSG, reply_markup=self.set_main_menu_kbd(message.from_user.id))
                return

            await state.update_data(suggest_uuid=suggest.uuid)
            txt = prepare_review_txt(suggest)
            await state.update_data(text=txt)

            await message.answer(QUESITON_REVIEW_MSG+txt, reply_markup=QUESTION_REVIEW_KBD, parse_mode='HTML')
            await state.set_state(SuggestReviewState.waiting_for_question_review)
        
        @self.router.callback_query(F.data.startswith("review_"))
        async def handle_review_answer(callback: CallbackQuery, state: FSMContext):
            answer = callback.data.split('_')[1]
            if answer == good_review:
                suggest_uuid = await state.get_value("suggest_uuid")
                logging.info("Selected good question button for %s suggest", suggest_uuid)

                self.suggest_service.mark_as_correct(suggest_uuid, callback.from_user.id)

                await callback.message.edit_text(FINISH_QUESTION_REVIEW_MSG)
                # await callback.message.answer(FINISH_QUESTION_REVIEW_MSG, reply_markup=self.set_main_menu_kbd(callback.from_user.id))
                await callback.answer()
                await state.clear()
            elif answer == bad_review:
                txt = await state.get_value("text")
                await callback.message.edit_text(txt, parse_mode='HTML')

                await callback.message.answer(BAD_QUESTION_REVIEW_MSG, reply_markup=CANCEL_KBD)
                await state.set_state(SuggestReviewState.waiting_for_bad_question_comment)
            elif answer == improve_review:
                txt = await state.get_value("text")
                await callback.message.edit_text(txt, parse_mode='HTML')

                await callback.message.answer(IMPROVE_QUESTION_REVIEW_MSG, reply_markup=CANCEL_KBD)
                await state.set_state(SuggestReviewState.waiting_for_improve_question_comment)
            elif answer == dont_know_review:
                await callback.message.edit_text(FINISH_QUESTION_REVIEW_MSG)
                await callback.answer()
                await state.clear()
        

        @self.router.message(SuggestReviewState.waiting_for_bad_question_comment)
        async def handle_bad_question_comment(message: Message, state: FSMContext):
            suggest_uuid = await state.get_value("suggest_uuid")
            logging.info("selected bad question button for %s suggest", suggest_uuid)
            
            self.suggest_service.mark_as_bad(suggest_uuid, message.text, message.from_user.id)

            await message.answer(FINISH_QUESTION_REVIEW_MSG, reply_markup=self.set_main_menu_kbd(message.from_user.id))
            await state.clear()
        

        @self.router.message(SuggestReviewState.waiting_for_improve_question_comment)
        async def handle_improve_question_comment(message: Message, state: FSMContext):
            suggest_uuid = await state.get_value("suggest_uuid")
            logging.info("selected improve question button for %s suggest", suggest_uuid)

            self.suggest_service.mark_as_improve(suggest_uuid, message.text, message.from_user.id)

            await message.answer(FINISH_QUESTION_REVIEW_MSG, reply_markup=self.set_main_menu_kbd(message.from_user.id))
            await state.clear()


        # level_ selected
        @self.router.callback_query(F.data.startswith("level_"))
        async def handle_level_callback(callback: CallbackQuery):
            level = callback.data.split('_')[1]  # level_1 -> 1
            logging.info("user(%s) selected %s level", callback.from_user.username, level)

            self.user_service.set_knowledge_level(callback.from_user.id, int(level))

            response = LEVEL_ORIENTED_RESPONSE_MSG[level]

            await callback.message.edit_text(response)
            await callback.message.answer(FIRST_LESSON_TAKE_OFFER_MSG, reply_markup=self.set_main_menu_kbd(callback.from_user.id))
            await callback.answer()

    def set_main_menu_kbd(self, telegram_id: int) -> ReplyKeyboardMarkup:
        kbd = MAIN_MENU_KBD.model_copy(deep=True)

        user = self.user_service.get_by_telegram_id(telegram_id)
        if user and user.role == ADMIN:
            add_reply_keyboard_button(kbd, question_review)
        
        return kbd


def prepare_review_txt(suggest: Suggest) -> str:
    txt = f"<blockquote>{suggest.question}</blockquote>\n\n"
    for i in range(0, len(suggest.answers)):
        answer = suggest.answers[i]

        if i == suggest.correct_id:
            txt += f"✅{answer}\n"
        else:
            txt += f"❌{answer}\n"
    
    return txt
