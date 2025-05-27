from fastapi import APIRouter, HTTPException
from fastapi.params import Header
from pydantic import ValidationError

from settings import settings
from .bot import bot, dispatcher


bot_rt = APIRouter(prefix="/telegram/bot")


@bot_rt.post("/webhook", tags=["Telegram"])
async def bot_webhook(
    update: dict,
    secret_key_header: str = Header(None, alias="X-Telegram-Bot-Api-Secret-Token"),
):
    if not secret_key_header or secret_key_header != settings.SECRET_KEY:
        raise HTTPException(403, "Secret token invalid.")
    try:
        await dispatcher.feed_webhook_update(bot, update)
    except ValidationError:
        raise HTTPException(400, "Invalid update data.")
