from aiogram import Bot, Dispatcher

from settings import settings

from .handlers.commands import commands_bot_rt
from .handlers.files import files_bot_rt

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dispatcher = Dispatcher()
dispatcher.include_router(commands_bot_rt)
dispatcher.include_router(files_bot_rt)
