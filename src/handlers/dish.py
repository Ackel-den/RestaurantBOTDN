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
async def add_dish_to_list(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    name = await state.get_data()
    if await rq.check_dish(name['name'], message.from_user.id):
        await message.answer("Это блюдо уже есть в списке")
    else:
        await rq.set_new_dish(name['name'], message.from_user.id)
        await message.answer("Блюдо успешо создано!")
    await state.clear()
    await message.answer('Вот что ещё можно сделать:', reply_markup=kb.menu)


# Удаление блюда
@router.callback_query(F.data.startswith('dish_delete:'))
async def delete_dish(callback: CallbackQuery):
    dish = callback.data.split(':')[1]
    await callback.message.edit_text(f'Блюдо {dish} успешно удалено', reply_markup=kb.menu)
    await rq.delete_dish(dish, callback.from_user.id)