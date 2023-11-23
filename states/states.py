from aiogram.filters.state import StatesGroup, State

class DataState(StatesGroup):
    choosing_sex = State()
    choosing_age = State()
    choosing_name = State()