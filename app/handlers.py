import asyncio
import datetime

from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

import settings

router = Router()
time = datetime.datetime.now()
setting = settings.Settings()
start_time = datetime.datetime.strptime(setting.time_start, "%H:%M")
end_time = datetime.datetime.strptime(setting.time_end, "%H:%M")


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Вы запустили ресторанного бота!")

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Существующие команды: "
                         "\n/start - запуск бота"
                         "\n/help - список команд"
                         "\n/time - узнать, работает ли ресторан")

@router.message(Command("time"))
async def cmd_time(message: Message):
    await message.answer("Время: " + str(time.strftime("%H:%M")))
    if  start_time.time() <= time.time() <= end_time.time():
        await message.answer("Ресторан открыт! Ждём Вас!"
                             "\nМы работаем с "+ start_time.strftime("%H:%M")
                             +" до "+end_time.strftime("%H:%M"))
    else:
        await message.answer("В данный момент ресторан закрыт!"
                             "\nМы работаем с "+ start_time.strftime("%H:%M")
                             +" до "+end_time.strftime("%H:%M"))


