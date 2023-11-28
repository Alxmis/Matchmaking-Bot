from aiogram.filters.state import StatesGroup, State

class DataState(StatesGroup):
    choosing_sex = State()
    choosing_age = State()
    choosing_name = State()
    fin_main_info = State()
    choosing_interest = State()
    change_name = State()
    change_age = State()
    change_sex = State()

class MainState(StatesGroup):
    in_main = State()
    talking = State()