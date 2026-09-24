import asyncio
import logging

asyncio.set_event_loop(asyncio.new_event_loop())

from aiogram import Bot, Dispatcher

from config import TOKEN
from pyrogram_app import app
from db.connection_manager import init_db, close_db

from handlers.commands.start import router as start_router
from handlers.commands.blacklist import router as blacklist_router
from handlers.commands.block import router as block_router
from handlers.commands.unblock import router as unblock_router
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
    await app.start()
    await init_db()
    print("Bot is running")


async def on_shutdown():
    if getattr(app, "is_initialized", False) and app.is_connected:
        try:
            await app.stop(block=False)
        except Exception as e:
            print(f"Error while stopping Pyrogram: {e}")

    await close_db()


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.include_router(start_router)
    dp.include_router(blacklist_router)
    dp.include_router(block_router)
    dp.include_router(unblock_router)
    dp.include_router(form_router)
    dp.include_router(decision_router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())