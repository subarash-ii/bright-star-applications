from datetime import datetime

from pyrogram_app import app
from pyrogram.errors import UsernameInvalid, UsernameOccupied, PeerIdInvalid


def remove_at(text):
    if text.startswith("@"):
        return text.replace("@", "")

    return text


def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
        return True
    except ValueError:
        return False


async def get_id_by_username(username: str):
    user = await app.get_users(username)
    return user.id


async def is_user_exists(id_or_username):
    try:
        await app.get_users(id_or_username)
        return True
    except:
        return False