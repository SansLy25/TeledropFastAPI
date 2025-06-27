from core.db import get_session
import re


def escape_markdown(text: str):
    return re.sub(r"([_*\[\]()~`>#+\-=|{}\.!])", r"\\\1", text)


def replace_slash(text: str):
    """
    Телеграм воспринимает текст со слешем как ссылки, поэтому заменяем
    на похожий символ
    """
    return text.replace("/", "∕")


async def get_db_session_for_bot():
    session_gen = get_session()
    return await session_gen.__anext__()
