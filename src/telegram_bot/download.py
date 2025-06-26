from storage.service import FileService
from telegram_bot.bot import bot


async def telegram_download_file(file, version_num, user, session):
    version = await FileService.get_version(file, version_num, session)
    if file.is_telegram_photo:
        method = bot.send_photo
    else:
        method = bot.send_document

    await method(user.telegram_id, version.telegram_file_id)