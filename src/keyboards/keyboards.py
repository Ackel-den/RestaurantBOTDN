from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


# Клавиатура главного меню
menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🍜Добавить блюдо', callback_data='create_dish')],
    [InlineKeyboardButton(text='🗒️Список блюд', callback_data='list_dish')]
])


category_create_dish = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='☕️Завтрак', callback_data='category:Завтрак'), InlineKeyboardButton(text= '🍛Обед',callback_data='category:Обед')],
    [InlineKeyboardButton(text='🥗Ужин', callback_data='category:Ужин'), InlineKeyboardButton(text='🍩Десерт', callback_data='category:Десерт')],
])

category_list_dish = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='☕️Завтрак', callback_data='category_list:Завтрак'), InlineKeyboardButton(text= '🍛Обед',callback_data='category_list:Обед')],
    [InlineKeyboardButton(text='🥗Ужин', callback_data='category_list:Ужин'), InlineKeyboardButton(text='🍩Десерт', callback_data='category_list:Десерт')],
    [InlineKeyboardButton(text='🏠Главное меню',callback_data='menu')]
])


# Клавиатура меню блюда
async def dish_menu(name):
    menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🗒️Посмотреть ингредиенты', callback_data=f'ingredient_list:{name}')],
        [InlineKeyboardButton(text='🧂Добавить ингредиент', callback_data=f'dish_{name}')],
        [InlineKeyboardButton(text='📝Изменить ингредиент', callback_data=f'ingredient_set:{name}')],
        [InlineKeyboardButton(text='📋Изменить описание блюда', callback_data=f'description:{name}')],
        [InlineKeyboardButton(text='❌Убрать ингредиент', callback_data=f'ingredient_delete:{name}')],
        [InlineKeyboardButton(text='🚫УДАЛИТЬ БЛЮДО🚫', callback_data=f'dish_delete:{name}')],
        [InlineKeyboardButton(text='⬅️Список блюд', callback_data='list_dish')]
    ])
    return menu


# Клавиатура на повторное создание ингредиента
async def continue_add_ing(dish_name):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='✅Да', callback_data= f'ingredient_yes:{dish_name}'))
    keyboard.add(InlineKeyboardButton(text='❌Нет', callback_data= 'menu'))
    return keyboard.adjust(2).as_markup()


# Клавиатура на удаление ингредиента
async def ingredient_list_delete(dish_name, ingredients):
    keyboard = InlineKeyboardBuilder()
    for ing in ingredients:
        keyboard.row(InlineKeyboardButton(text=ing.name, callback_data=f'delete_{ing.id}_{dish_name}'))
    keyboard.row(InlineKeyboardButton(text='⬅️Назад', callback_data=f'dishmenu_{dish_name}'))
    return keyboard.as_markup()


# Клавиатура на изменения ингредиента
async def ingredient_list_set(dish_name, ingredients):
    keyboard = InlineKeyboardBuilder()
    for ing in ingredients:
        keyboard.row((InlineKeyboardButton(text=ing.name, callback_data=f'set_{ing.id}_{dish_name}')))
    keyboard.row(InlineKeyboardButton(text='⬅️Назад', callback_data=f'dishmenu_{dish_name}'))
    return keyboard.as_markup()