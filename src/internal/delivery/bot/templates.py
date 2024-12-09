# TODO: make levels more objective and refactor messages
NEW_USER_RESPONSE = (
    "Привет! Этот бот позволяет изучить новые и закрепить старые знания в исламе"
    "(на данный момент только Фикх, но мы не планируем останавливаться).\n\n"
    "Позволь узнать твой примерный уровень, чтобы подбирать релевантные вопросы. Выбери цифру от 1 до 5, где:\n\n"
    "1️⃣ - Слышал про намаз и пост, но не знаю как их соблюдать. Вообще, я новенький и хочу все изучить)\n"
    "2️⃣ - Совершаю намаз, держу пост, а их что может что-то нарушить?\n"
    "3️⃣ - Знаю основные сунны и фарзы, но у меня очень расплывчатые знания\n"
    "4️⃣ - Знаю адабы/сунны/фарзы намаза/омовения/поста/брака/торговых отношений, но некоторые вещи забылись и "
    "мне хочется просто повторить\n"
    "5️⃣ - Закончил высшее образование или медресе, хочу повторить все"
)

START_HANDLER_RESPONSE = (
    "Привет! Этот бот позволяет изучить новые и закрепить старые знания в исламе.\n"
    "Основные команды бота:\n"
    "/help - помощь в использовании\n"
    "/lesson - начать урок\n"
    "/statistic - моя статистика\n"
    "/faq - частые вопросы\n"
    "/feedback - оставить отзыв\n"
)

LEVEL_ORIENTED_RESPONSE = {
    "1": "Круто, что ты хочешь изучать религию. Главное не останавливайся",
    "2": "Хорошо, что ты выполняешь столпы ислама. Данный бот тебе поможет изучить и узнать про ислам больше",
    "3": "something",
    "4": "something",
    "5": "Я смотрю ты знаток своего дела. Поэтому, для тебя дополнительно хотим предложить возможность добавлять и "
         "проверять вопросы перед тем, как они попадут к пользователям. \n\n"
         "Если тебе это интересно, то напиши кому-то из нас: @IskanderShakiroff или @Timer_han",
}

FIRST_LESSON_TAKE_OFFER = (
    "Если ты готов изучение, то можно начать учиться /lesson))\n\n"
    "Каждый урок состоит из 10 вопросов. В вопросе есть 4 варианта ответа, один из которых правильный.\n"
    "✅При правильном ответе, перейдешь на следующий\n"
    "❌Если ответишь неправильно, бот добавит описание правильного ответа\n"
    "‼️Советуем его прочитать и запомнить, потому что бот еще раз задаст этот вопрос через некоторое время"
)