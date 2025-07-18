import asyncio

from aiogram import Bot, Dispatcher

import settings
from app.handlers import router

setting = settings.Settings()

async def main():
    bot = Bot(token = setting.bot_token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")