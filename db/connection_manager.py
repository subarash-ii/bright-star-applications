import aiosqlite

from config import DB_NAME

_db_connection: aiosqlite.Connection | None = None


async def init_tables(db: aiosqlite.Connection):
    await db.execute('''
        CREATE TABLE IF NOT EXISTS blacklist (
            id INTEGER NOT NULL,
            username TEXT NOT NULL
        )
    ''')

    await db.execute('''
        CREATE TABLE IF NOT EXISTS active (
            id INTEGER NOT NULL,
            username TEXT NOT NULL
        )
    ''')

    await db.commit()


async def init_db():
    global _db_connection
    _db_connection = await aiosqlite.connect(DB_NAME)
    _db_connection.row_factory = aiosqlite.Row

    await init_tables(_db_connection)


async def close_db():
    if _db_connection:
        await _db_connection.close()


def get_db() -> aiosqlite.Connection:
    if _db_connection is None:
        raise RuntimeError("Database connection is not initialized. Call init_db() first.")

    return _db_connection


def with_db(func):
    async def wrapper(*args, **kwargs):
        return await func(get_db(), *args, **kwargs)

    return wrapper