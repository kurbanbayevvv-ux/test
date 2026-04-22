import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers.start import router as start_router
from handlers.balance import router as balance_router
from handlers.card import router as card_router
from handlers.otkazma import router as otkazma_router

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # router ulash
    dp.include_router(start_router)
    dp.include_router(balance_router)
    dp.include_router(card_router)
    dp.include_router(otkazma_router)

    print("Bot ishga tushdi...")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
