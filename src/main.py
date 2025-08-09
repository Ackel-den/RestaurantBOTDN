import asyncio

from aiogram import Bot, Dispatcher

import settings
from handlers import router
from database.models import async_main

setting = settings.Settings()
bot = Bot(token=setting.bot_token)
dp = Dispatcher()


async def main():
    await async_main()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
