from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import ADMINS
from db.blacklist.queries import get_all_blocked

router = Router()


@router.message(Command("blacklist"))
async def command_blacklist_handler(message: Message):
    if message.from_user.id not in ADMINS:
        return

    all_blocked = await get_all_blocked()

    if len(all_blocked) == 0:
        await message.answer("В чёрном списке ещё никого нет.")
        return

    text = (
        "Чёрный список: \n\n"
    )

    for blocked in all_blocked:
        text += f"@{blocked["username"]}\n"

    await message.answer(text)