import logging

from aiogram import F, Router
from aiogram.types import TelegramObject, Voice, VideoNote, Sticker, Message, PhotoSize

from telegram_bot.utils import escape_markdown as _, replace_slash
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
        "name": getattr(message_object, "file_name", None),
        "is_telegram_photo": isinstance(message_object, PhotoSize)
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
async def file_upload_handler(message: Message):
    session = await get_db_session_for_bot()
    user = await UserService.get_by_tg_id(session=session, tg_id=message.from_user.id)
    current_folder = await FolderService.get_current_folder(user, session)

    message_file = await get_file_telegram_object(message)
    file_data = await extract_data_from_telegram_object(message_file)
    action, file = await FileService.update_or_create(
        session, file_data, current_folder
    )

    if action == "created":
        text = (f"✅ *{_(file.name)}* сохранен\n\n"
                f"🧭 Путь: _{_(replace_slash(file.path))}_")
    else:
        text = (f"🔄 *{_(file.name)}* был обновлен\n\n"
                f"❗️ Cтарая версия файла доступна в *Версиях*")

    await message.reply(text, parse_mode="MarkdownV2", disable_web_page_preview=True)
