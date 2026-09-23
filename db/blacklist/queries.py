import aiosqlite

from db.connection_manager import with_db


@with_db
async def is_user_blocked(db: aiosqlite.Connection, user_id: int):
    async with db.execute("SELECT 1 FROM blacklist WHERE id = ? LIMIT 1", (user_id,)) as cursor:
        row = await cursor.fetchone()

        return row is not None


@with_db
async def get_all_blocked(db: aiosqlite.Connection):
    async with db.execute("SELECT * FROM blacklist") as cursor:
        return await cursor.fetchall()


@with_db
async def add_user(db: aiosqlite.Connection, user_id: int, username: str):
    async with db.execute("INSERT OR IGNORE INTO blacklist (id, username) VALUES (?, ?)", (user_id, username)):
        await db.commit()


@with_db
async def delete_by_id(db: aiosqlite.Connection, user_id: int):
    async with db.execute("DELETE FROM blacklist WHERE id = ?", (user_id,)) as cursor:
        await db.commit()

        if cursor.rowcount > 0:
            return True
        else:
            return False