import re
from collections import defaultdict

from schemas.ingredients import Ingredients

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


def default_factory():
    return "Такого блюда нет"


list_of_dish = defaultdict(default_factory)


# команда для создания блюда
@router.message(Command("create"))
async def cmd_create(message: Message):
    try:
        name = split_message(message)[0]
    except TypeError:
        await message.answer(
            "Неверный ввод, проверьте верно ли вы отправили сообщение!"
        )
        return

    if name in list_of_dish:
        await message.answer("Это блюдо уже есть в списке")
        return

    list_of_dish[name] = list()
    print(list_of_dish)


# добавление ингредиента в блюдо
@router.message(Command("add"))
async def cmd_add(message: Message):
    try:
        ingredients = split_message(message)
        dish_name = ingredients[0]
    except TypeError:
        await message.answer(
            "Неверный ввод, проверьте верно ли вы отправили сообщение!"
        )
        return
    except IndexError:
        await message.answer(
            "Неверный ввод, проверьте верно ли вы отправили сообщение!"
        )
        return

    ingredients.pop(0)

    if check_dish_list(dish_name):
        if len(ingredients) < 3:
            await message.answer(
                "Неверный ввод\n"
                "\nКак добавить: "
                '\n/add "название блюда" "название ингредиента" '
                '"вес ингредиента" "единица измерения" '
            )
            return
        elif len(ingredients) == 3:
            name, weight, measure = ingredients
            new_ingr = Ingredients(name=name, weight=weight, measure=measure)
            list_of_dish[dish_name].append(new_ingr)
            print(list_of_dish)
            return
    await message.answer("Такого блюда не существует!")


# команда для списка ингредиентов
@router.message(Command("get"))
async def cmd_get(message: Message):
    try:
        name = split_message(message)[0]
    except TypeError:
        await message.answer(
            "Неверный ввод, проверьте верно ли вы отправили сообщение!"
        )
        return

    if check_dish_list(name):
        await message.answer(f'Блюдо "{name}": {get_ingredients(name)}')
        return
    await message.answer("Такого блюда не существует!")


@router.message(Command("reduce"))
async def cmd_reduce(message: Message):
    try:
        dish_name = split_message(message)[0]
        ing_name = split_message(message)[1]
        value = split_message(message)[2]
    except TypeError:
        await message.answer(
            "Неверный ввод, проверьте верно ли вы отправили сообщение!"
        )
        return

    for i in list_of_dish[dish_name]:
        if i.name == ing_name:
            i.weight -= float(value)
            if i.weight == 0 or i.weight < 0:
                list_of_dish[dish_name].remove(i)

    print(list_of_dish[dish_name])


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
    if len(split_message) == 0:
        return
    return split_message
