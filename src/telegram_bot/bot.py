from settings import settings
from aiogram import Bot, Dispatcher
from .handlers.commands import commands_bot_rt

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dispatcher = Dispatcher()
dispatcher.include_router(commands_bot_rt)