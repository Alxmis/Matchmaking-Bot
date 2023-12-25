from aiogram.filters.state import StatesGroup, State

class DataState(StatesGroup):
    choosing_sex = State()
    choosing_age = State()
    choosing_name = State()
    choosing_interest = State()
    fin_main_info = State()
    change_name = State()
    change_age = State()
    change_sex = State()
    change_interest = State()

class MainState(StatesGroup):
    in_main = State()
    talking = State()
    ch_profile = State()
    ch_age = State()
    ch_name = State()
    ch_sex = State()
    ch_interest = State()