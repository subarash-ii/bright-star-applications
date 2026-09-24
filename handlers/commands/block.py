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
        await message.answer("Введите имя пользователя после комнады /block")

    username = remove_at(command.args.split(" ")[0])

    is_exists = await is_user_exists(username)

    if not is_exists:
        await message.answer(f"Пользователя с именем @{username} не существует.")
        return

    id = await get_id_by_username(username)

    is_blocked = await is_user_blocked(id)

    if is_blocked:
        await message.answer(f"Пользователь @{username} уже находиться в чёрном списке.")
        return

    await block_user(id, username)
    await message.answer(f"@{username} был успешно заблкирован.")