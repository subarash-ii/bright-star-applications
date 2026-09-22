import aiosqlite

from config import DB_NAME


async def is_user_blocked(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row

        async with db.execute("SELECT 1 FROM blacklist WHERE id = ? LIMIT 1", (user_id,)) as cursor:
            row = await cursor.fetchone()

            return row is not None


async def add_user(user_id: int, username: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT OR IGNORE INTO blacklist (id, username) VALUES (?, ?)",
            (user_id, username)
        )

        await db.commit()