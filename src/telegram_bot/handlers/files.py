from aiogram import F, Router
from aiogram.types import (
    TelegramObject,
    Voice,
    VideoNote,
    Sticker,
    Message,
    PhotoSize
)

from storage.service import FolderService, FileService
from telegram_bot.utils import get_db_session_for_bot
from users.service import UserService

files_bot_rt = Router()


async def get_file_telegram_object(message: Message):
    content_type = message.content_type
    if content_type == "photo":
        return message.photo[-1]

    return getattr(message, content_type)

async def extract_data_from_telegram_object(
        message_object: TelegramObject,
) -> dict:

    file_data = {
        "telegram_file_id": message_object.file_id,
        "size": getattr(message_object, "file_size", None),
        "type": getattr(message_object, "mime_type", None),
    }

    TYPES_CONVERT = {
        Voice: "audio/ogg",
        VideoNote: "video/mp4",
        Sticker: "image/webp",
        PhotoSize: "image/jpeg",
    }

    current_mime_type = file_data["type"]
    file_data["type"] = current_mime_type or TYPES_CONVERT[type(message_object)]

    return file_data


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
    current_folder = await FolderService.get_current_folder(user, session)

    message_file = await get_file_telegram_object(message)
    file_data = await extract_data_from_telegram_object(message_file)
    file = await FileService.create(session, file_data, current_folder)
    await message.answer(file.name)






