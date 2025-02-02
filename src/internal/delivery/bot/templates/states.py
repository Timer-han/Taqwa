from aiogram.fsm.state import StatesGroup, State


class SuggestQuestionState(StatesGroup):
    waiting_for_question = State()
    waiting_for_answers = State()
    waiting_for_description = State()
    waiting_for_difficulty = State()

class SuggestReviewState(StatesGroup):
    waiting_for_question_review = State()
    waiting_for_bad_question_comment = State()
    waiting_for_improve_question_comment = State()
