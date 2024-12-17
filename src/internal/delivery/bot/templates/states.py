from aiogram.fsm.state import StatesGroup, State


class SuggestQuestionState(StatesGroup):
    waiting_for_question = State()
    waiting_for_answers = State()
