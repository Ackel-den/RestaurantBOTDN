from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from schemas.fsm import AddIngredient, SetIngredient
from schemas.ingredients import Ingredients
from database import request as rq
import keyboards.keyboards as kb

router = Router()


# Эта функция работает, если пользователь согласился на повторное добавление ингредиента
@router.callback_query(F.data.startswith('ingredient_yes:'))
async def add_ingredient_again(callback: CallbackQuery, state: FSMContext):
    await state.update_data(dish_name=callback.data.split(':')[1])
    await callback.message.edit_text(
        f'Введите название ингредиента, который хотите добавить в блюдо "{callback.data.split(':')[1]}"')
    await state.set_state(AddIngredient.name)


# Создание ингредиента
@router.callback_query(F.data.startswith('dish_'))
async def add_ingredient_dish_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(dish_name=callback.data.split('_')[1])
    await callback.message.edit_text(f'Введите название ингредиента, который хотите добавить в блюдо '
                                     f'"{callback.data.split('_')[1]}"')
    await state.set_state(AddIngredient.name)


@router.message(AddIngredient.name)
async def add_ingredient_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    name = await state.get_data()
    if await rq.check_ingedient(name['dish_name'], name['name'], message.from_user.id):
        await message.answer(f"Ингредиент {name['name']} уже есть в списке!",
                             reply_markup=await kb.dish_menu(name['dish_name']))
    else:
        await state.set_state(AddIngredient.weight)
        await message.answer('Введите колличество ингредиента')


@router.message(AddIngredient.weight)
async def add_ingredient_weight(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await state.set_state(AddIngredient.measure)
    await message.answer("Введите меру измерения (например: мл, л, кг, г)")


@router.message(AddIngredient.measure)
async def add_ingredient_measure(message: Message, state: FSMContext):
    await state.update_data(measure=message.text)
    ingredient = await state.get_data()
    new_ingr = Ingredients(name=ingredient['name'], weight=float(ingredient['weight']), measure=ingredient['measure'])
    await rq.set_new_ing(ingredient['dish_name'], new_ingr, message.from_user.id)
    await message.answer("Ингредиент добавлен в список!")
    await state.clear()
    await message.answer('\n\nХотите добавить ещё ингредиент?',
                         reply_markup=await kb.continue_add_ing(ingredient['dish_name']))


# Список ингредиентов
@router.callback_query(F.data.startswith('ingredient_list:'))
async def get_ingredient_list(callback: CallbackQuery):
    dish_name = callback.data.split(':')[1]
    await callback.message.edit_text(
            f'Блюдо "{dish_name}": {await rq.get_ingredient_list_str(dish_name, callback.from_user.id)}',
            reply_markup=await kb.dish_menu(dish_name))


# Удаление ингредиента
@router.callback_query(F.data.startswith('delete_'))
async def delete_ingredient(callback: CallbackQuery):
    id = callback.data.split('_')[1]
    dish_name = callback.data.split('_')[2]
    await callback.message.edit_text('Ингредиент успешно удалён', reply_markup=await kb.dish_menu(dish_name))
    await rq.delete_ingredient(id)


# Изменение ингредиента
@router.callback_query(F.data.startswith('set_'))
async def set_ingedient(callback: CallbackQuery, state: FSMContext):
    await state.update_data(id = callback.data.split('_')[1])
    await state.update_data(dish_name = callback.data.split('_')[2])
    await state.set_state(SetIngredient.set_weight)
    await callback.message.edit_text('Введите новое значение ингредиента\n\n'
                                     'Предупрждение: если вы введёте 0, или меньше, ингредиент удалится')


@router.message(SetIngredient.set_weight)
async def set_new_weight(message: Message, state: FSMContext):
    ing = await state.get_data()
    weight = message.text
    if weight.isnumeric():
        await rq.set_new_weight(ing['id'], float(weight))
        await message.answer('Новое значение установлено', reply_markup=await kb.dish_menu(ing['dish_name']))
        await state.clear()
    else:
        await message.answer('Значение должно быть числом', reply_markup=await kb.dish_menu(ing['dish_name']))
        await state.clear()

