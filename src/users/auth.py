import http
from typing import Annotated

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.security.http import HTTPBase

from telegram_webapp_auth.auth import TelegramAuthenticator
from telegram_webapp_auth.auth import WebAppUser
from telegram_webapp_auth.auth import generate_secret_key
from telegram_webapp_auth.errors import InvalidInitDataError

from settings import settings
from users.models import User


telegram_authentication_schema = HTTPBase()


def get_telegram_authenticator() -> TelegramAuthenticator:
    secret_key = generate_secret_key(settings.BOT_SECRET_KEY)
    return TelegramAuthenticator(secret_key)


def get_current_user(
    auth_cred: HTTPAuthorizationCredentials = Depends(telegram_authentication_schema),
    telegram_authenticator: TelegramAuthenticator = Depends(get_telegram_authenticator),
) -> WebAppUser:
    try:
        init_data = telegram_authenticator.validate(auth_cred.credentials)
    except InvalidInitDataError:
        raise HTTPException(
            status_code=http.HTTPStatus.FORBIDDEN,
            detail="Access denied.",
        )
    except Exception:
        raise HTTPException(
            status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Server error.",
        )

    if init_data.user is None:
        raise HTTPException(
            status_code=http.HTTPStatus.FORBIDDEN,
            detail="Access denied.",
        )

    return init_data.user


UserDp = Annotated[User, Depends(get_current_user)]