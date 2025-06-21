from core.db import get_session

async def get_db_session_for_bot():
    session_gen = get_session()
    return await session_gen.__anext__()