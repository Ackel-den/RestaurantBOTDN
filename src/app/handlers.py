from datetime import datetime

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from src import settings

router = Router()
setting = settings.Settings()
start_time = datetime.strptime(setting.time_start, "%H:%M").time()
end_time = datetime.strptime(setting.time_end, "%H:%M").time()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Вы запустили ресторанного бота!")


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "Существующие команды: "
        "\n/start - запуск бота"
        "\n/help - список команд"
        "\n/time - узнать, работает ли ресторан"
    )


@router.message(Command("time"))
async def cmd_time(message: Message):
    now = datetime.now().time()
    await message.answer("Время: " + str(now.strftime("%H:%M")))

    if start_time <= now <= end_time:
        await message.answer(
            f"Ресторан открыт! Ждём Вас!\nМы работаем с {start_time.strftime("%H:%M")} до {end_time.strftime("%H:%M")}"
        )
    else:
        await message.answer(
            f"В данный момент ресторан закрыт!\nМы работаем с {start_time.strftime("%H:%M")} до {end_time.strftime("%H:%M")}"
        )
