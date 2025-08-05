import re

from schemas.ingredients import Ingredients

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


list_of_dish = dict()


# команда для создания блюда
@router.message(Command("create"))
async def cmd_create(message: Message):
    name = await check_message(message, 1)

    if name is None:
        return

    name = name[0]

    if name in list_of_dish:
        await message.answer("Это блюдо уже есть в списке")
        return

    list_of_dish[name] = list()
    await message.answer("Блюдо успешо создано!")
    print(list_of_dish)


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

    if dish_name in list_of_dish:
        for i in list_of_dish[dish_name]:
            if i.name == name:
                await message.answer("Такой ингредиент уже есть в списке!")
                return
        else:
            new_ingr = Ingredients(name=name, weight=weight, measure=measure)
            list_of_dish[dish_name].append(new_ingr)
            await message.answer("Ингредиент добавлен в список!")
    else:
        await message.answer("Такого блюда не существует!")


# команда для списка ингредиентов
@router.message(Command("get"))
async def cmd_get(message: Message):
    name = await check_message(message, 1)

    if name is None:
        return

    name = name[0]

    if name in list_of_dish:
        await message.answer(f'Блюдо "{name}": {get_ingredients(name)}')
    else:
        await message.answer("Такого блюда не существует!")


# Установление значения для ингредиента
@router.message(Command("set"))
async def cmd_set(message: Message):
    dish = await check_message(message, 3)

    if dish is None:
        return

    dish_name, ing, value = dish
    value = float(value)

    if dish_name in list_of_dish:
        for i in list_of_dish[dish_name]:
            if i.name == ing:
                if value <= 0:
                    list_of_dish[dish_name].remove(i)
                    await message.answer(f'Ингредиент "{i.name}" удалён из списка!')
                elif value > 0:
                    i.weight = value
                    await message.answer(
                        f'Количество ингредиента "{i.name}" теперь = {i.weight}'
                    )
                break
        else:
            await message.answer("Такого ингредиента в списке нет!")
    else:
        await message.answer("Такого блюда не существует!")


async def check_message(message: Message, n: int) -> list[str] | None:
    text_message = split_message(message)
    print(len(text_message))
    if n > len(text_message) or len(text_message) == 0:
        await message.answer(
            "Неверный ввод, проверьте, верно ли вы отправили сообщение!"
        )
        return None

    return text_message


# получение ингредиентов блюда
def get_ingredients(name: str):
    list_of_ingr = ""

    if list_of_dish[name]:
        n = 0
        for i in list_of_dish[name]:
            n += 1
            list_of_ingr += f"\n{n}. {i.name} - {i.weight} {i.measure}"
    else:
        list_of_ingr = "\nВ блюде пока нет ингредиентов"

    return list_of_ingr


# "вытаскиевание" нужных слов с помощью кавычек
def quotes_finder(text):
    return re.findall(r'"([^"]*)"', text)


# разделение строки на массив строк
def split_message(message: Message):
    split_message = quotes_finder(message.text)
    return split_message
