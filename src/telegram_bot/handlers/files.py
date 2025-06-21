from aiogram import F, Router
from aiogram.types import Message, TelegramObject

from storage.models import Folder
from storage.service import FolderService
from telegram_bot.utils import get_db_session_for_bot
from users.service import UserService

files_bot_rt = Router()


async def get_file_telegram_object(message: Message):
    content_type = message.content_type
    if content_type == "photo":
        return message.photo[-1]

    return getattr(message, content_type)

async def convert_telegram_object_to_model(
    message_object: TelegramObject,
):
    pass


@files_bot_rt.message(
    (
        F.content_type.in_(
            {
                "document",
                "photo",
                "video",
                "audio",
                "voice",
                "video_note",
                "sticker",
                "animation",
            }
        )
    )
)
async def file_handler(message: Message):
    session = await get_db_session_for_bot()
    user = await UserService.get_by_tg_id(
        session=session,
        tg_id=message.from_user.id
    )
    current_folder = await FolderService.get()
    message_file = await get_file_telegram_object(message)
    file = await convert_telegram_object_to_model(message_file)



