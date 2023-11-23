from aiogram import types
from aiogram.filters import Command, StateFilter
from aiogram import F, Router
from aiogram.filters.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from main import bot
import keyboards.keyboards as kb
from states.states import DataState

router = Router()
class UserData(StatesGroup):
    age = State()
    sex = State()
    name = State()
@router.message(Command("start"))
async def sex(message: types.Message, state: FSMContext):
    await message.answer("Привет! Я бот для поиска анонимного собеседника! Пожалуйста, укажите ваш пол.", reply_markup = kb.kb_sex)
    (await state.set_state(DataState.choosing_sex)

@router.message(DataState.choosing_sex))
async def sex(message: types.Message, state: FSMContext):
    await message.answer("Я такого пола не знаю(", reply_markup=kb.kb_sex)
    await state.set_state(DataState.choosing_sex)
@router.message(DataState.choosing_sex, F.text.in_(["Мужчина", 'Женщина']))
async def age(message: types.Message, state: FSMContext):
    await message.answer("Супер! Теперь укажите свой возраст.")
    await state.set_state(DataState.choosing_age)
@router.message(DataState.choosing_age)
async def age(message: types.Message, state: FSMContext):
    await message.answer("И последнее: как Вас зовут?")
    await state.set_state(DataState.choosing_name)

@router.message(DataState.choosing_name)
async def fin(message: types.Message, state: FSMContext):
    await message.answer("Отлично, проверьте ваши данные!\n Имя: ... \n Возраст: ... \n Пол: ... \n", reply_markup=)
