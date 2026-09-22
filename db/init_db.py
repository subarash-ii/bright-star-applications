import aiosqlite

from config import DB_NAME


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
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