import html
from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from config import ADMINS
from util import get_id_by_username, is_user_exists, remove_at
from db.blacklist.queries import block_user, is_user_blocked

router = Router()


@router.message(Command("block"))
async def command_block_handler(message: Message, command: CommandObject):
    if message.from_user.id not in ADMINS:
        return

    if command.args is None:
        await message.answer("⚠️ <b>Укажите имя пользователя:</b>\n<code>/block username</code>")
        return

    raw_username = command.args.split(" ")[0]
    username = remove_at(raw_username)
    safe_username = html.escape(username)

    is_exists = await is_user_exists(username)

    if not is_exists:
        await message.answer(f"❌ Пользователь <b>@{safe_username}</b> не найден.")
        return

    user_id = await get_id_by_username(username)

    is_blocked = await is_user_blocked(user_id)

    if is_blocked:
        await message.answer(f"⚠️ Пользователь <b>@{safe_username}</b> уже находится в чёрном списке.")
        return

    await block_user(user_id, username)
    await message.answer(f"🚫 Пользователь <b>@{safe_username}</b> успешно заблокирован.")