from fastapi import APIRouter

from .bot import bot, dispatcher


bot_rt = APIRouter(prefix="/telegram/bot")


@bot_rt.post("/webhook")
async def bot_webhook(update: dict):
    await dispatcher.feed_webhook_update(bot, update)