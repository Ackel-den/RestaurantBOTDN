from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

per_page = 6

# Клавиатура со списком блюд
async def paginated_dish_list(dish_list, page):
    start = page * per_page
    end = start + per_page
    currrent_list = dish_list[start:end]
    keyboard = InlineKeyboardBuilder()

    for dish in currrent_list:
        keyboard.add(InlineKeyboardButton(text=dish.name, callback_data=f'dishmenu_{dish.name}'))

    keyboard.adjust(2)
    keyboard.row(InlineKeyboardButton(text='📋Назад к списку', callback_data='list_dish'))

    if page == 0 and end <= len(dish_list):
        keyboard.row(InlineKeyboardButton(text='➡️', callback_data=f'page:{page+1}'))
    elif page!=0 and end >= len(dish_list):
        keyboard.row(InlineKeyboardButton(text='⬅️', callback_data=f'page:{page-1}'))
    elif end < len(dish_list):
        keyboard.row(InlineKeyboardButton(text='⬅️', callback_data=f'page:{page-1}'),
                     InlineKeyboardButton(text='➡️', callback_data=f'page:{page+1}'))

    return keyboard.as_markup()

