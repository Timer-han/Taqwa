# from aiogram import Bot, Dispatcher
# from aiogram.enums.parse_mode import ParseMode
# from aiogram.fsm.storage.memory import MemoryStorage
#
# from src.internal.storage.user import UserRepository
# from src.internal.service.user import UserService
# from src.config.config import EnvironmentSettings
# from src.internal.delivery.bot.bot import BotHandler
#
#
# class Application:
#     def __init__(self, env: EnvironmentSettings):
#         user_repository = UserRepository()
#         user_service = UserService(user_repository)
#         # user_handler = UserHandler("/user", user_service)
#
#         bot = Bot(token=env.BOT_TOKEN, parse_mode=ParseMode.HTML)
#         dp = Dispatcher(storage=MemoryStorage())
#
#         bot_handlers = BotHandler(bot, user_service)
#
#         dp.include_router(bot_handlers.router)
#
# # def start(self):
# #     app = FastAPI(openapi_url="/core/openapi.json", docs_url="/core/docs")
# #
# #     app.include_router(self.user_handler.router)
