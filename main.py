import asyncio
from config import YOUR_BOT
from aiogram import Bot, Dispatcher  # pip install -U aiogram
from aiogram.enums import ParseMode
from logic.bmi import bmi_router
from logic.gfr import gfr_router
from admin.command import command_router
from logic.calendar import calendar_router
from admin.admin import admin_router
from loguru import logger  # pip install loguru


TOKEN = YOUR_BOT


logger.add('ihfo.log', format="{time} {level} {message}", level="INFO",
           rotation="1 week", compression="zip")


async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(admin_router)
    dp.include_router(bmi_router)
    dp.include_router(gfr_router)
    dp.include_router(command_router)
    dp.include_router(calendar_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
