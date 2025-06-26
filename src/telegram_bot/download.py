from aiogram.exceptions import TelegramBadRequest

from storage.service import FileService
from telegram_bot.bot import bot

async def telegram_download_file(file, version_num, user, session):
    version = await FileService.get_version(file, version_num, session)
    await bot.send_document(user.telegram_id, version.telegram_file_id)