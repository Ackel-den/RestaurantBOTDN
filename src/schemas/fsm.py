from aiogram.fsm.state import StatesGroup, State


class CreateDish(StatesGroup):
    name = State()
    description = State()

class AddIngredient(StatesGroup):
    name = State()
    weight = State()
    measure = State()

class SetIngredient(StatesGroup):
    set_weight = State()