from schemas.fsm import CreateDish
from database import request as rq
import keyboards.keyboards as kb

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

router = Router()


# Создание блюда
@router.callback_query(F.data=='create_dish')
async def cmd_create(callback: CallbackQuery, state: FSMContext):
    await state.set_state(CreateDish.name)
    await callback.answer('')
    await callback.message.edit_text('Введите название блюда')


@router.message(CreateDish.name)
async def name_dish(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    name = await state.get_data()
    if await rq.check_dish(name['name'], message.from_user.id):
        await message.answer("Это блюдо уже есть в списке")
    else:
        await message.answer('Выберите категорию для блюда:', reply_markup=kb.category_create_dish)


@router.callback_query(F.data.startswith('category:'))
async def dish_category(callback: CallbackQuery, state: FSMContext):
    await state.update_data(category = callback.data.split(':')[1])
    dish = await state.get_data()
    await rq.set_new_dish(dish['name'], dish['category'], callback.from_user.id)
    await callback.message.answer("Блюдо успешо создано!")
    await state.clear()
    await callback.message.answer('Вот что ещё можно сделать:', reply_markup=kb.menu)


#Добавление описания
@router.callback_query(F.data.startswith('description:'))
async def add_desription(callback: CallbackQuery, state: FSMContext):
    await state.update_data(dish=callback.data.split(':')[1])
    await callback.message.answer('Напишите описание готовки блюда')
    await state.set_state(CreateDish.description)


@router.message(CreateDish.description)
async def set_description(message: Message, state: FSMContext):
    dish = await state.get_data()
    await rq.set_description(message.from_user.id, dish['dish'], message.text)
    await message.answer('Описание успешно добавлено!', reply_markup=await kb.dish_menu(dish['dish']))


# Удаление блюда
@router.callback_query(F.data.startswith('dish_delete:'))
async def delete_dish(callback: CallbackQuery):
    dish = callback.data.split(':')[1]
    await callback.message.edit_text(f'Блюдо {dish} успешно удалено', reply_markup=kb.menu)
    await rq.delete_dish(dish, callback.from_user.id)