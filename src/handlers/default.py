from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

import database.request as rq


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer("Привет! Вы запустили ресторанного бота! Чтобы вызвать меню, пропишите: /menu")
