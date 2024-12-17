from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


start_lesson = "📝Начать урок"
bot_help = "❓Как пользоваться"
profile = "🏡Профиль"
question_suggest = "📚Предложить вопрос"
question_cancel = "Отменить вопрос"

MAIN_MENU_KBD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=start_lesson), KeyboardButton(text=bot_help)],
        [KeyboardButton(text=profile), KeyboardButton(text=question_suggest)],
    ],
    resize_keyboard=True,
)

KNOWLEDGE_LEVEL_DETERMINE_KBD = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text="1", callback_data="level_1"),
        InlineKeyboardButton(text="2", callback_data="level_2"),
        InlineKeyboardButton(text="3", callback_data="level_3"),
        InlineKeyboardButton(text="4", callback_data="level_4"),
        InlineKeyboardButton(text="5", callback_data="level_5"),
    ]]
)

QUESTION_SUGGEST_KBD = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=question_cancel)]],
    resize_keyboard=True,
)
