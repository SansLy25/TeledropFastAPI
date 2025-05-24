import logging
import time

from fastapi import FastAPI, Request, APIRouter

from core.db import init_db
from settings import settings
from telegram_bot.bot import bot
from telegram_bot.views import bot_rt
from users.views import user_rt


logging.basicConfig(level=logging.INFO)

app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc")


def create_main_router():
    router = APIRouter(prefix='/api')
    router.include_router(bot_rt)
    router.include_router(user_rt)
    return router


app.include_router(create_main_router())


async def register_webhook():
    webhook_info = await bot.get_webhook_info()
    full_url = settings.HOST_NAME + "/api/telegram/bot/webhook"

    if webhook_info.url != full_url:
        await bot.set_webhook(
            url=full_url,
            drop_pending_updates=True,
            secret_token=settings.SECRET_KEY,
        )

    logging.info("Bot started")


async def unregister_webhook():
    await bot.delete_webhook()
    logging.info("Bot stopped, webhook deleted")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.on_event("startup")
async def start():
    await init_db()
    await register_webhook()


@app.on_event("shutdown")
async def shutdown():
    await unregister_webhook()
