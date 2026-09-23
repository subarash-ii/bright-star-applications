from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import ADMINS

router = Router()


@router.message(Command("blacklist"))
async def command_blacklist_handler(message: Message):
    if message.from_user.id not in ADMINS:
        return

    await message.answer("Blacklist")