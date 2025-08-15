from mimetypes import inited

from database.models import async_session
from database.models import User, Dish, Ingredient
from sqlalchemy import select


# Добавление пользователя в БД
async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))  # noqa

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


# Добавление блюда в БД
async def set_new_dish(name, tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        dish = await session.scalar(
            select(Dish).where(Dish.name == name, Dish.user_id == user.id)
        )

        if not dish:
            session.add(Dish(name=name, user_id=user.id))
            await session.commit()


# Добавление ингредиента в БД
async def set_new_ing(dish, ing, tg_id):
    async with async_session() as session:
        ingredient = await session.scalar(
            select(Ingredient).where(Ingredient.name == ing.name)
        )
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not ingredient:
            dish = await session.scalar(
                select(Dish).where(Dish.name == dish, Dish.user_id == user.id)
            )
            session.add(
                Ingredient(
                    dish=dish.id, name=ing.name, weight=ing.weight, measure=ing.measure
                )
            )
            await session.commit()


# Установление нового значения для ингредиента
async def set_new_weight(id, weight):
    async with async_session() as session:

        ing = await session.scalar(
            select(Ingredient).where(Ingredient.id == id)
        )
        if weight <= 0:
            await session.delete(ing)
            await session.commit()
            return

        ing.weight = weight
        await session.commit()


# Возвращает список ингредиентов строкой
async def get_ingredient_list_str(name: str, tg_id):
    ingredients = ""
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id==tg_id))
        dish = await session.scalar(
            select(Dish).where(Dish.name == name, Dish.user_id == user.id)
        )
        list_of_ingr = await session.scalars(
            select(Ingredient).where(Ingredient.dish == dish.id)
        )

        if list_of_ingr:
            n = 0
            for i in list_of_ingr:
                n += 1
                ingredients += f"\n{n}. {i.name} - {i.weight} {i.measure}"
            if n== 0:
                ingredients = "\nВ блюде пока нет ингредиентов"

        return ingredients


# Получить список ингредиентов
async def get_ingredient_list(dish_name, tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id==tg_id))
        dish = await session.scalar(select(Dish).where(Dish.user_id==user.id, Dish.name==dish_name))
        ingredient_list = await session.scalars(select(Ingredient).where(Ingredient.dish==dish.id))
        return ingredient_list.all()


# Получить список блюд
async def get_dish_list(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id==tg_id))
        dish_list = await session.scalars(select(Dish).where(Dish.user_id==user.id))
        return dish_list.all()


# Удаление блюда и ингредиентов
async def delete_dish(dish_name, tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id==tg_id))
        dish = await session.scalar(select(Dish).where(Dish.user_id==user.id, Dish.name==dish_name))
        if dish:
            ingredients = await session.scalars(select(Ingredient).where(Ingredient.dish==dish.id))
            if ingredients:
                for ing in ingredients:
                    await session.delete(ing)
                    await session.commit()
            await session.delete(dish)
            await session.commit()


# Удаление ингредиента
async def delete_ingredient(id):
    async with async_session() as session:
        ingredient = await session.scalar(select(Ingredient).where(Ingredient.id==id))
        await session.delete(ingredient)
        await session.commit()


# Проверка существует ли такое блюдо
async def check_dish(name, tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        name = await session.scalar(
            select(Dish).where(Dish.name == name, Dish.user_id == user.id)
        )
        return bool(name)


# Проверка существует ли  такой ингредиент
async def check_ingedient(dish, name, tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        dish = await session.scalar(
            select(Dish).where(Dish.name == dish, Dish.user_id == user.id)
        )
        ingredient = await session.scalar(
            select(Ingredient).where(
                Ingredient.dish == dish.id, Ingredient.name == name
            )
        )
        return bool(ingredient)
