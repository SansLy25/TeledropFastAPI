from core.db import get_session
import re


def escape_markdown(text):
    return re.sub(r'([_*\[\]()~`>#+\-=|{}\.!])', r'\\\1', text)


async def get_db_session_for_bot():
    session_gen = get_session()
    return await session_gen.__anext__()
