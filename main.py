import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import TOKEN
from db.connection_manager import init_db, close_db
from handlers.commands.start import router as start_router
from handlers.commands.blacklist import router as blacklist_router
from handlers.form import router as form_router
from handlers.decision import router as decision_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    filename="bot.log",
    filemode="a",
    encoding="utf-8"
)

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def on_startup():
    await init_db()
    print("Bot is running")


async def on_shutdown():
    await close_db()


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.include_router(start_router)
    dp.include_router(blacklist_router)
    dp.include_router(form_router)
    dp.include_router(decision_router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())