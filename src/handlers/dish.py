import re
from collections import defaultdict

from schemas.ingredients import Ingredients

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


list_of_dish = defaultdict()


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
    ingredients: [str] = await check_message(message, 4)

    if ingredients is None:
        await message.answer(
            "Неверный ввод\n"
            "\nКак добавить: "
            '\n/add "название блюда" "название ингредиента" '
            '"вес ингредиента" "единица измерения" '
        )
        return

    dish_name = ingredients[0]
    ingredients.pop(0)

    if check_dish_list(dish_name):
        name, weight, measure = ingredients
        new_ingr = Ingredients(name=name, weight=weight, measure=measure)
        list_of_dish[dish_name].append(new_ingr)
        await message.answer("Ингредиент добавлен в список!")
        return

    await message.answer("Такого блюда не существует!")


# команда для списка ингредиентов
@router.message(Command("get"))
async def cmd_get(message: Message):
    name = await check_message(message, 1)

    if name is None:
        return

    name = name[0]

    if check_dish_list(name):
        await message.answer(f'Блюдо "{name}": {get_ingredients(name)}')
        return

    await message.answer("Такого блюда не существует!")


@router.message(Command("reduce"))
async def cmd_reduce(message: Message):
    text_message = await check_message(message, 4)

    if text_message is None:
        await message.answer(
            "Неверный ввод\n"
            "\nКак уменьшить количество ингредиента : "
            '\n/reduce "название блюда" "название ингредиента" '
            '"на сколько хотите уменьшить вес"  '
        )
        return

    dish_name = text_message[0]
    ing_name = text_message[1]
    value = text_message[2]

    for i in list_of_dish[dish_name]:
        if i.name == ing_name:
            i.weight -= float(value)
            await message.answer(
                f'Количество ингредиента "{i.name}" теперь = {i.weight}'
            )
            if i.weight == 0 or i.weight < 0:
                list_of_dish[dish_name].remove(i)
                await message.answer("Ингредиент удалён из списка!")
        else:
            await message.answer("Такого ингредиента в списке нет!")

    print(list_of_dish[dish_name])


async def check_message(message: Message, n: int) -> []:
    text_message = split_message(message)

    if len(text_message) == 0 or n < len(text_message):
        await message.answer(
            "Неверный ввод, проверьте, верно ли вы отправили сообщение!"
        )
        return None

    return text_message


# проверка на наличие имени в словаре
def check_dish_list(name: str):
    if name in list_of_dish:
        return True
    else:
        return False


# получение ингредиентов блюда
def get_ingredients(name: str):
    if len(list_of_dish[name]) == 0:
        x = "\nВ блюде пока нет ингредиентов"
    else:
        n = 0
        for i in list_of_dish[name]:
            n += 1
            x = f"\n{n}. {i.name} - {i.weight} {i.measure}"
    return x


# "вытаскиевание" нужных слов с помощью кавычек
def quotes_finder(text):
    return re.findall(r'"([^"]*)"', text)


# разделение строки на массив строк
def split_message(message: Message):
    split_message = quotes_finder(message.text)
    return split_message
