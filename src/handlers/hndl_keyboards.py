from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from keyboards import paginated_keyboards as pg
from keyboards import keyboards as kb
from database import request as rq

router = Router()


@router.message(Command('menu'))
async def cmd_menu(message: Message):
    await message.answer('Вот что можно сделать',reply_markup=kb.menu)


@router.callback_query(F.data=='menu')
async def menu(callback: CallbackQuery):
    await callback.message.edit_text('Вот что можно сделать',reply_markup=kb.menu)


# Клавиатура списка блюд
@router.callback_query(F.data=='list_dish')
async def choose_dish(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выберите блюдо из списка:',
                         reply_markup=await pg.paginated_dish_list(await rq.get_dish_list(callback.from_user.id), 0))


@router.callback_query(F.data.startswith('page:'))
async def paginate(callback: CallbackQuery):
    page = int(callback.data.split(':')[1])
    await callback.message.edit_reply_markup(reply_markup=
                                             await pg.paginated_dish_list(await rq.get_dish_list(callback.from_user.id), page))
    await callback.answer('')


# Клавиатура меню блюда
@router.callback_query(F.data.startswith('dishmenu_'))
async def dish_menu_kb(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Выберите что вы хотите сделать:',
                                     reply_markup=await kb.dish_menu(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('ingredient_set:'))
async def set_ing_list(callback: CallbackQuery):
    dish_name = callback.data.split(':')[1]
    await callback.answer()
    await callback.message.edit_text('Количество какого ингредиента вы хотите изменить?',
                                     reply_markup=
                                     await kb.ingredient_list_set(dish_name,
                                                                  await rq.get_ingredient_list(dish_name, callback.from_user.id)))


@router.callback_query(F.data.startswith('ingredient_delete:'))
async def delete_ing_list(callback: CallbackQuery):
    dish_name = callback.data.split(':')[1]
    await callback.answer()
    await callback.message.edit_text('Какой ингредиент вы хотите удалить?',
                                     reply_markup=
                                     await kb.ingredient_list_delete(dish_name,
                                                                  await rq.get_ingredient_list(dish_name,
                                                                                               callback.from_user.id)))
