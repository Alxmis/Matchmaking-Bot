from aiogram import types
from aiogram.filters import Command
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
import keyboards.keyboards as kb
from states.states import DataState, MainState
from search_bot_backend.database_requests import BotDB
from main import bot

router = Router() # инит роутера, чтоб не кидать все вы один
#-----------------------------------------------------------------основная часть-----------------------------------------------------------------------
@router.message(Command("start"))
async def sex(message: types.Message, state: FSMContext):
    if (BotDB.user_exists(message.from_user.id)):
        await state.set_state(MainState.in_main)
        await message.answer(f"С возвращением, {BotDB.get_name(message.from_user.id)}!", reply_markup=kb.kb_main) #если у нас уже был юзер в бд
        return
    await message.answer("Привет! Я бот для поиска анонимного собеседника! Пожалуйста, укажите ваш пол.", reply_markup = kb.kb_sex)
    await state.set_state(DataState.choosing_sex)
@router.message(DataState.choosing_sex, F.text.in_(["Мужской", 'Женский']))
async def age(message: types.Message, state: FSMContext):
    await state.update_data(choosen_sex = message.text.lower())
    markup = types.ReplyKeyboardRemove()
    await message.answer("Супер! Теперь укажите свой возраст.", reply_markup=markup)
    await state.set_state(DataState.choosing_age)
@router.message(DataState.choosing_sex)
async def sex(message: types.Message, state: FSMContext):
    await message.answer("Я такого пола не знаю(", reply_markup=kb.kb_sex)
    await state.set_state(DataState.choosing_sex)
@router.message(DataState.choosing_age)
async def age(message: types.Message, state: FSMContext):
    await state.update_data(choosen_age=message.text.lower())
    await message.answer("И последнее: как Вас зовут?")
    await state.set_state(DataState.choosing_name)

@router.message(DataState.choosing_name)
async def fin(message: types.Message, state: FSMContext):
    await state.update_data(choosen_name=message.text.lower())
    user = await state.get_data()
    await message.answer(f"Отлично, проверьте ваши данные!\n Имя: {user['choosen_name']} \n Возраст: {user['choosen_age']} \n Пол: {user['choosen_sex']} \n", reply_markup=kb.kb_ch)
    await state.set_state(DataState.fin_main_info)
#---------------------------------------------------------------------------часть проверки корректности--------------------------------------------------
@router.message(DataState.fin_main_info)
async def change(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardRemove()
    if message.text == "Изменить имя":
        await message.answer("Укажите новое имя.", reply_markup = markup)
        await state.set_state(DataState.change_name)
    elif message.text == "Изменить пол":
        await message.answer("Укажите пол.", reply_markup = kb.kb_sex)
        await state.set_state(DataState.change_sex)
    elif message.text == "Изменить возраст":
        await message.answer("Укажите возраст.", reply_markup = markup)
        await state.set_state(DataState.change_age)
    else:
        await message.answer("Основная информация получена, давайте теперь поймем, чем вы увлекаетесь, чтобы подобрать вам мобеседника с максимально общими интересами!\n"
                         "\nНапишите три интересующих вас занятия через пробел (это важно!)")
        await state.set_state(DataState.choosing_interest)
@router.message(DataState.change_sex, F.text.in_(["Мужской", 'Женский']))
async def change_sex(message: types.Message, state: FSMContext):
    await state.update_data(choosen_sex=message.text.lower())
    user = await state.get_data()
    await message.answer(f"Отлично, проверьте ваши данные!\n Имя: {user['choosen_name']} \n Возраст: {user['choosen_age']} \n Пол: {user['choosen_sex']} \n", reply_markup=kb.kb_ch)
    await state.set_state(DataState.fin_main_info)
@router.message(DataState.change_sex)
async def change_sex(message: types.Message, state: FSMContext):
    await message.answer("Я такого пола не знаю(", reply_markup=kb.kb_sex)

@router.message(DataState.change_name)
async def change_name(message: types.Message, state: FSMContext):
    await state.update_data(choosen_name=message.text.lower())
    user = await state.get_data()
    await message.answer(f"Отлично, проверьте ваши данные!\n Имя: {user['choosen_name']} \n Возраст: {user['choosen_age']} \n Пол: {user['choosen_sex']} \n", reply_markup=kb.kb_ch)
    await state.set_state(DataState.fin_main_info)
@router.message(DataState.change_age)
async def change_age(message: types.Message, state: FSMContext):
    await state.update_data(choosen_age=message.text.lower())
    user = await state.get_data()
    await message.answer(f"Отлично, проверьте ваши данные!\n Имя: {user['choosen_name']} \n Возраст: {user['choosen_age']} \n Пол: {user['choosen_sex']} \n", reply_markup=kb.kb_ch)
    await state.set_state(DataState.fin_main_info)
#----------------------------------------------------------------------------------сбор интересов-----------------------------------------------------------
@router.message(DataState.choosing_interest)
async def interests(message: types.Message, state: FSMContext):
    await state.update_data(interests = message.text.strip().split())
    user = await state.get_data()
    BotDB.add_user(message.chat.id, user['choosen_sex'], user['choosen_age'], user['choosen_name'], user['interests'][0], user['interests'][1], user['interests'][2])
    await message.answer("Супер, регистрация пройдена! Теперь вам доступен поиск собеседника", reply_markup = kb.kb_main)
    await state.set_state(MainState.in_main)

@router.message(MainState.in_main)
async def main(message: types.Message, state: FSMContext):
    if (message.text == 'Найти собеседника'):
        await bot.send_message(text = "Ищем собеседника...", chat_id = message.chat.id)
        partner = BotDB.get_partner(message.chat.id)
        print(partner)
        print(message.chat.id)
        if (partner != None):
            await bot.send_message(text="Собеседник найден, общайтесь!", chat_id=message.chat.id, reply_markup = kb.kb_cancel)
            await bot.send_message(text="Собеседник найден, общайтесь!", chat_id=partner, reply_markup = kb.kb_cancel)
            BotDB.update_status(partner, 0)
            BotDB.update_status(message.chat.id, 0)
            BotDB.add_dialogue(partner, message.chat.id)
        else:
            await bot.send_message(text="Очередь пока пустая, ждите!", chat_id=message.chat.id, reply_markup = kb.kb_cancel)
        await state.set_state(MainState.talking)


@router.message(MainState.talking)
async def talk(message: types.Message, state: FSMContext):
    get_dia = BotDB.get_dialogues(message.chat.id)
    if (message.text != "Закончить сессию" and len(get_dia) != 0):
        await bot.send_message(text = message.text, chat_id = get_dia[0])
    elif (message.text == "Закончить сессию"):
        await bot.send_message(text="Сессия закончена", chat_id=message.chat.id, reply_markup = kb.kb_main)
        get_dia = BotDB.get_dialogues(message.chat.id)
        if (len(get_dia) != 0):
            await bot.send_message(text="Сессия закончена", chat_id=get_dia[0], reply_markup = kb.kb_main)
            BotDB.remove_dialogues(message.chat.id)
            BotDB.remove_dialogues(get_dia[0])
        await state.set_state(MainState.in_main)
    elif (len(get_dia) == 0):
        await bot.send_message(text="Вас никто не слышит", chat_id=message.chat.id)