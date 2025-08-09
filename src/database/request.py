from database.models import async_session
from database.models import User, Dish, Ingredient
from sqlalchemy import select


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))  # noqa

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def set_new_dish(name, tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        dish = await session.scalar(
            select(Dish).where(Dish.name == name, Dish.user_id == user.id)
        )

        if not dish:
            session.add(Dish(name=name, user_id=user.id))
            await session.commit()


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


async def set_new_weight(dish, ing, weight):
    async with async_session() as session:
        dish = await session.scalar(select(Dish).where(Dish.name == dish))
        ing = await session.scalar(
            select(Ingredient).where(Ingredient.dish == dish.id, Ingredient.name == ing)
        )
        if weight <= 0:
            await session.delete(ing)
            await session.commit()
            return

        ing.weight = weight
        await session.commit()


async def get_ingredients(name: str, tg_id):
    ingredients = ""
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
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
        else:
            ingredients = "\nВ блюде пока нет ингредиентов"

        return ingredients


async def check_dish(name, tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        name = await session.scalar(
            select(Dish).where(Dish.name == name, Dish.user_id == user.id)
        )
        return bool(name)


async def check_ingedient(dish, name):
    async with async_session() as session:
        dish = await session.scalar(select(Dish).where(Dish.name == dish))
        ingredient = await session.scalar(
            select(Ingredient).where(
                Ingredient.dish == dish.id, Ingredient.name == name
            )
        )
        return bool(ingredient)
