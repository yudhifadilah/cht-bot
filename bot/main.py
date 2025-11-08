import asyncio
import logging
from aiogram import Dispatcher
from bot.handlers import dp, bot

async def main():
    logging.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
