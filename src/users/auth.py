import http
from typing import Annotated

from fastapi import Depends, HTTPException, Request
from fastapi.security import APIKeyHeader, HTTPBasic
from telegram_webapp_auth.auth import (
    TelegramAuthenticator,
    WebAppUser,
    generate_secret_key,
)
from telegram_webapp_auth.errors import InvalidInitDataError

from core.db import SessionDp
from settings import settings
from users.models import User
from users.service import UserService


class TMAAuth(APIKeyHeader):
    async def __call__(self, request: Request) -> str:
        auth_header = await super().__call__(request)
        if not auth_header:
            raise HTTPException(403, "Auth header not provided.")

        if len(auth_header.split()) != 2:
            raise HTTPException(403, "Auth creds incorrect.")

        return auth_header.split()[1]


telegram_authentication_schema = TMAAuth(
    scheme_name="tma",
    description="Authorization based on Telegram Init Data",
    name="Authorization",
)


def get_telegram_authenticator() -> TelegramAuthenticator:
    secret_key = generate_secret_key(settings.TELEGRAM_BOT_TOKEN)
    return TelegramAuthenticator(secret_key)


def get_telegram_user_init_data(
    auth_cred: str = Depends(telegram_authentication_schema),
    telegram_authenticator: TelegramAuthenticator = Depends(get_telegram_authenticator),
) -> WebAppUser:
    try:
        init_data = telegram_authenticator.validate(auth_cred)
    except InvalidInitDataError:
        raise HTTPException(
            status_code=http.HTTPStatus.FORBIDDEN,
            detail="Access denied.",
        )

    if init_data.user is None:
        raise HTTPException(
            status_code=http.HTTPStatus.FORBIDDEN,
            detail="Access denied.",
        )

    return init_data.user


async def get_or_create_user(
    session: SessionDp,
    user_init_data: WebAppUser = Depends(get_telegram_user_init_data),
) -> User:
    user = await UserService.get_by_tg_id(session=session, tg_id=user_init_data.id)
    if user is None:
        return await UserService.create(session=session, user_in=user_init_data)

    return user


UserDp = Annotated[User, Depends(get_or_create_user)]
