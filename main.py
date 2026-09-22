import asyncio

from aiogram import Bot, Dispatcher

from config import TOKEN
from handlers.start import router as start_router
from handlers.form import router as form_router
from handlers.process_decision import router as decision_router

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    print("Bot is running")

    dp.include_router(start_router)
    dp.include_router(form_router)
    dp.include_router(decision_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())