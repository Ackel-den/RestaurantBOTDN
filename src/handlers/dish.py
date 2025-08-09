import re

from schemas.ingredients import Ingredients
from database import request as rq

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


# команда для создания блюда
@router.message(Command("create"))
async def cmd_create(message: Message):
    name = await check_message(message, 1)

    if name is None:
        return

    name = name[0]

    if await rq.check_dish(name, message.from_user.id):
        await message.answer("Это блюдо уже есть в списке")
        return
    else:
        await rq.set_new_dish(name, message.from_user.id)
        await message.answer("Блюдо успешо создано!")


# добавление ингредиента в блюдо
@router.message(Command("add"))
async def cmd_add(message: Message):
    ingredients: list[str] = await check_message(message, 4)

    if ingredients is None:
        await message.answer(
            "Неверный ввод\n"
            "\nКак добавить: "
            '\n/add "название блюда" "название ингредиента" '
            '"вес ингредиента" "единица измерения" '
        )
        return

    dish_name, name, weight, measure = ingredients

    if await rq.check_dish(dish_name, message.from_user.id):
        if await rq.check_ingedient(dish_name, name):
            await message.answer(f"Ингредиент {name} уже есть в списке!")
        else:
            if weight.isnumeric():
                new_ingr = Ingredients(name=name, weight=float(weight), measure=measure)
                await rq.set_new_ing(dish_name, new_ingr, message.from_user.id)
                await message.answer("Ингредиент добавлен в список!")
            else:
                await message.answer("Количество ингредиента должно состоять из числа")
    else:
        await message.answer("Такого блюда не существует!")


# команда для списка ингредиентов
@router.message(Command("get"))
async def cmd_get(message: Message):
    name = await check_message(message, 1)

    if name is None:
        return

    name = name[0]

    if await rq.check_dish(name, message.from_user.id):
        await message.answer(
            f'Блюдо "{name}": {await rq.get_ingredients(name, message.from_user.id)}'
        )
    else:
        await message.answer("Такого блюда не существует!")


# Установление значения для ингредиента
@router.message(Command("set"))
async def cmd_set(message: Message):
    dish = await check_message(message, 3)

    if dish is None:
        return

    dish_name, ing, value = dish

    if value.isnumeric():
        if await rq.check_dish(dish_name, message.from_user.id):
            if await rq.check_ingedient(dish_name, ing):
                await rq.set_new_weight(dish_name, ing, float(value))
                if float(value) > 0:
                    await message.answer(f'Значение ингредиента "{ing}" теперь {value}')
                else:
                    await message.answer("Ингредиент удалён из списка!")
            else:
                await message.answer("Такого ингредиента нет в списке!")
        else:
            await message.answer("Такое блюдо не существует!")
    else:
        await message.answer("Количество ингредиента должно состоять из числа")


async def check_message(message: Message, n: int) -> list[str] | None:
    text_message = split_message(message)
    print(len(text_message))
    if n > len(text_message) or len(text_message) == 0:
        await message.answer(
            "Неверный ввод, проверьте, верно ли вы отправили сообщение!"
        )
        return None

    return text_message


# "вытаскиевание" нужных слов с помощью кавычек
def quotes_finder(text):
    return re.findall(r'"([^"]*)"', text)


# разделение строки на массив строк
def split_message(message: Message):
    split_message = quotes_finder(message.text)
    return split_message
