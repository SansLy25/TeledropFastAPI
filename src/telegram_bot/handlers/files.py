from aiogram import Router
from aiogram import F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from users.service import UserService
from core.db import get_session


files_bot_rt = Router()

@files_bot_rt.message((F.content_type.in_({
    'document', 'photo', 'video', 'audio', 'voice', 'video_note', 'sticker', 'animation'
})))
async def cmd_start(message: Message):
    session_gen = get_session()
    session = await session_gen.__anext__()
    user = await UserService.get_by_tg_id(session=session, tg_id=message.from_user.id)

    await message.answer(str(user))