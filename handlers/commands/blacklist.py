import html
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
        await message.answer("📜 <b>Чёрный список пуст.</b>")
        return

    text = "⛔ <b>Чёрный список:</b>\n\n"

    for blocked in all_blocked:
        clean_username = html.escape(str(blocked["username"]))
        text += f"• @{clean_username}\n"

    await message.answer(text)