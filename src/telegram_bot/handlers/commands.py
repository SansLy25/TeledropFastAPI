from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

commands_bot_rt = Router()

@commands_bot_rt.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет"
    )