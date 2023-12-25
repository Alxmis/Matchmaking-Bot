import time

from aiogram import F, Router
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

import keyboards.keyboards as kb
from main import bot
from search_bot_backend.database_requests import BotDB
from states.states import DataState, MainState

router = Router()  # инит роутера, чтоб не кидать все вы один


# -----------------------------------------------------------------основная часть-----------------------------------------------------------------------
@router.message(Command("start"))
async def sex(message: types.Message, state: FSMContext):
    if (BotDB.user_exists(message.from_user.id)):
        await state.set_state(MainState.in_main)
        await message.answer(f"С возвращением, {BotDB.get_name(message.from_user.id)}!",
                             reply_markup=kb.kb_main)  # если у нас уже был юзер в бд
        return
    await message.answer("Привет! Я бот для поиска анонимного собеседника! Пожалуйста, укажите ваш пол.",
                         reply_markup=kb.kb_sex)
    await state.set_state(DataState.choosing_sex)


@router.message(DataState.choosing_sex, F.text.in_(["Мужской", 'Женский']))
async def age(message: types.Message, state: FSMContext):
    await state.update_data(choosen_sex=message.text.lower())
    markup = types.ReplyKeyboardRemove()
    await message.answer("Супер! Теперь укажите свой возраст.", reply_markup=markup)
    await state.set_state(DataState.choosing_age)


@router.message(DataState.choosing_sex)
async def sex(message: types.Message, state: FSMContext):
    await message.answer("Я такого пола не знаю(", reply_markup=kb.kb_sex)
    await state.set_state(DataState.choosing_sex)


@router.message(DataState.choosing_age)
async def age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return message.answer("Введите число.")
    await state.update_data(choosen_age=message.text.lower())
    await message.answer("И последнее: как Вас зовут?")
    await state.set_state(DataState.choosing_name)


@router.message(DataState.choosing_name)
async def fin(message: types.Message, state: FSMContext):
    await state.update_data(choosen_name=message.text.lower())
    await message.answer(
        "Основная информация получена, давайте теперь поймем, чем вы увлекаетесь, чтобы подобрать вам cобеседника "
        "с максимально общими интересами!",
        parse_mode='markdown',
        reply_markup=kb.cats
    )
    await state.set_state(DataState.choosing_interest)


@router.message(DataState.choosing_interest)
async def choose_interests(message: types.Message, state: FSMContext):
    user = await state.get_data()

    try:
        user['interests']
    except:
        await state.update_data(interests=[])
        user = await state.get_data()

    if message.text in user['interests']:
        return await message.answer(f"Вы уже выбрали эту категорию, выберите еще {3 - len(user['interests'])}")
    elif message.text not in kb.cats_list:
        return await message.answer(f"Этой категории не существует, выберите из кнопок ниже:")
    elif len(user['interests']) < 3:
        await state.update_data(interests=user['interests'] + [message.text])
        user = await state.get_data()
    if len(user['interests']) == 3:
        BotDB.add_user(message.chat.id, user['choosen_sex'], user['choosen_age'], user['choosen_name'],
                       user['interests'][0], user['interests'][1], user['interests'][2])
    elif len(user['interests']) < 3:
        return await message.answer(f"{chr(10).join(user['interests'])}\n\nДобавлено, выберите ещё {3 - len(user['interests'])}")

    user = await state.get_data()
    await message.answer(
        f"Отлично, проверьте ваши данные! \nИмя: {user['choosen_name']} \nВозраст: {user['choosen_age']} \nПол: {user['choosen_sex']} \nИнтересы: \n{chr(10).join(user['interests'])} \n",
        reply_markup=kb.kb_ch)
    await state.set_state(DataState.fin_main_info)


# ---------------------------------------------------------------------------часть проверки корректности--------------------------------------------------
@router.message(DataState.fin_main_info)
async def change(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardRemove()
    if message.text == "Изменить имя":
        await message.answer("Укажите новое имя.", reply_markup=markup)
        await state.set_state(DataState.change_name)
    elif message.text == "Изменить пол":
        await message.answer("Укажите пол.", reply_markup=kb.kb_sex)
        await state.set_state(DataState.change_sex)
    elif message.text == "Изменить возраст":
        await message.answer("Укажите возраст.", reply_markup=markup)
        await state.set_state(DataState.change_age)
    elif message.text == "Изменить интересы":
        await message.answer("Выберите интересы из списка ниже.", reply_markup=kb.cats)
        await state.update_data(interests=[])
        await state.set_state(DataState.change_interest)
    else:
        await message.answer("Супер, регистрация пройдена! Теперь вам доступен поиск собеседника",
                             reply_markup=kb.kb_main)
        await state.set_state(MainState.in_main)


@router.message(DataState.change_sex, F.text.in_(["Мужской", 'Женский']))
async def change_sex(message: types.Message, state: FSMContext):
    await state.update_data(choosen_sex=message.text.lower())
    user = await state.get_data()
    await message.answer(
        f"Отлично, проверьте ваши данные! \nИмя: {user['choosen_name']} \nВозраст: {user['choosen_age']} \nПол: {user['choosen_sex']} \nИнтересы: \n{chr(10).join(user['interests'])} \n",
        reply_markup=kb.kb_ch)
    await state.set_state(DataState.fin_main_info)


@router.message(DataState.change_sex)
async def change_sex(message: types.Message, state: FSMContext):
    await message.answer("Я такого пола не знаю(", reply_markup=kb.kb_sex)


@router.message(DataState.change_name)
async def change_name(message: types.Message, state: FSMContext):
    await state.update_data(choosen_name=message.text.lower())
    user = await state.get_data()
    await message.answer(
        f"Отлично, проверьте ваши данные! \nИмя: {user['choosen_name']} \nВозраст: {user['choosen_age']} \nПол: {user['choosen_sex']} \nИнтересы: \n{chr(10).join(user['interests'])} \n",
        reply_markup=kb.kb_ch)
    await state.set_state(DataState.fin_main_info)


@router.message(DataState.change_age)
async def change_age(message: types.Message, state: FSMContext):
    await state.update_data(choosen_age=message.text.lower())
    user = await state.get_data()
    await message.answer(
        f"Отлично, проверьте ваши данные! \nИмя: {user['choosen_name']} \nВозраст: {user['choosen_age']} \nПол: {user['choosen_sex']} \nИнтересы: \n{chr(10).join(user['interests'])} \n",
        reply_markup=kb.kb_ch)
    await state.set_state(DataState.fin_main_info)


@router.message(DataState.change_interest)
async def change_interest(message: types.Message, state: FSMContext):
    user = await state.get_data()
    try:
        user['interests']
    except:
        await state.update_data(interests=[])
        user = await state.get_data()

    if message.text in user['interests']:
        return await message.answer(f"Вы уже выбрали эту категорию, выберите еще {3 - len(user['interests'])}")
    elif message.text not in kb.cats_list:
        return await message.answer(f"Этой категории не существует, выберите из кнопок ниже:")
    elif len(user['interests']) < 3:
        await state.update_data(interests=user['interests'] + [message.text])
        user = await state.get_data()
    if len(user['interests']) == 3:
        BotDB.update_interests(message.chat.id, user['interests'][0], user['interests'][1], user['interests'][2])
    elif len(user['interests']) < 3:
        return await message.answer(f"{chr(10).join(user['interests'])}\n\nДобавлено, выберите ещё {3 - len(user['interests'])}")

    user = await state.get_data()
    await message.answer(
        f"Отлично, проверьте ваши данные! \nИмя: {user['choosen_name']} \nВозраст: {user['choosen_age']} \nПол: {user['choosen_sex']} \nИнтересы: \n{chr(10).join(user['interests'])} \n",
        reply_markup=kb.kb_ch)
    await state.set_state(DataState.fin_main_info)


# ---------------------------------------------------------------------------главное меню--------------------------------------------------
@router.message(MainState.in_main)
async def main(message: types.Message, state: FSMContext):
    if message.text == 'Найти собеседника':
        await bot.send_message(text="Ищем собеседника...", chat_id=message.chat.id)
        partner = BotDB.get_partner(message.chat.id)
        print(partner)
        print(message.chat.id)
        time.sleep(2)
        if (partner != None):
            await bot.send_message(text="Собеседник найден, общайтесь!", chat_id=message.chat.id,
                                   reply_markup=kb.kb_cancel)
            await bot.send_message(text=f"Ваш собеседник: \nИмя: {BotDB.get_name(partner)} \nВозраст: {BotDB.get_age(partner)} \nПол: {BotDB.get_sex(partner)} \nИнтересы: \n{BotDB.get_interests(partner)} \n",
                                   chat_id=message.chat.id,
                                   reply_markup=kb.kb_cancel)
            await bot.send_message(text="Собеседник найден, общайтесь!", chat_id=partner, reply_markup=kb.kb_cancel)
            await bot.send_message(text=f"Ваш собеседник: \nИмя: {BotDB.get_name(message.chat.id)} \nВозраст: {BotDB.get_age(message.chat.id)} \nПол: {BotDB.get_sex(message.chat.id)} \nИнтересы: \n{BotDB.get_interests(message.chat.id)} \n",
                                   chat_id=partner,
                                   reply_markup=kb.kb_cancel)
            BotDB.update_status(partner, 0)
            BotDB.update_status(message.chat.id, 0)
            BotDB.add_dialogue(partner, message.chat.id)
        else:
            await bot.send_message(text="Собеседников пока нет, попробуйте позже!", chat_id=message.chat.id, reply_markup=kb.kb_cancel)
            time.sleep(2)
        await state.set_state(MainState.talking)

    elif message.text == 'Удалить меня из бота':
        BotDB.delete_user(message.chat.id)
        await state.clear()
        await message.answer('Вы были удалены. Нажмите на /start, чтобы пройти регистрацию заново', reply_markup=ReplyKeyboardRemove())

    elif message.text == 'Изменить профиль':
        await state.set_state(MainState.ch_profile)
        await message.answer(f"Выберите, что вы хотели бы изменить", reply_markup=kb.kb_ch)


@router.message(MainState.talking)
async def talk(message: types.Message, state: FSMContext):
    get_dia = BotDB.get_dialogues(message.chat.id)
    if message.text != "Закончить сессию" and len(get_dia) != 0:
        await bot.copy_message(get_dia[0], message.chat.id, message.message_id)
    elif message.text == "Закончить сессию":
        await bot.send_message(text="Сессия закончена", chat_id=message.chat.id, reply_markup=kb.kb_main)
        get_dia = BotDB.get_dialogues(message.chat.id)
        if len(get_dia) != 0:
            await bot.send_message(text="Собеседник закончил разговор", chat_id=get_dia[0])
            BotDB.remove_dialogues(message.chat.id)
            BotDB.remove_dialogues(get_dia[0])

        await bot.send_message(text="Идет возвращение в главное меню", chat_id=message.chat.id, reply_markup=ReplyKeyboardRemove())
        time.sleep(2)
        await bot.send_message(text="Вы возвращены в меню!", chat_id=message.chat.id, reply_markup=kb.kb_main)
        await state.set_state(MainState.in_main)
    elif len(get_dia) == 0:
        return await bot.send_message(text="Вас никто не слышит", chat_id=message.chat.id, reply_markup=kb.kb_cancel)


# ---------------------------------------------------------------------------часть редактирования профиля--------------------------------------------------
@router.message(MainState.ch_profile)
async def changing(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardRemove()
    if message.text == "Изменить имя":
        await message.answer("Укажите новое имя", reply_markup=markup)
        await state.set_state(MainState.ch_name)
    elif message.text == "Изменить пол":
        await message.answer("Укажите пол", reply_markup=kb.kb_sex)
        await state.set_state(MainState.ch_sex)
    elif message.text == "Изменить возраст":
        await message.answer("Укажите возраст", reply_markup=markup)
        await state.set_state(MainState.ch_age)
    elif message.text == "Изменить интересы":
        await message.answer("Выберите интересы из списка ниже", reply_markup=kb.cats)
        await state.update_data(interests=[])
        await state.set_state(MainState.ch_interest)
    else:
        await message.answer("Супер, вы возвращены в меню!", reply_markup=kb.kb_main)
        await state.set_state(MainState.in_main)


@router.message(MainState.ch_age)
async def change_age(message: types.Message, state: FSMContext):
    BotDB.update_age(message.chat.id, message.text)
    await message.answer(
        f"Отлично, проверьте ваши данные! \nИмя: {BotDB.get_name(message.chat.id)} \nВозраст: {BotDB.get_age(message.chat.id)} \nПол: {BotDB.get_sex(message.chat.id)} \nИнтересы: \n{BotDB.get_interests(message.chat.id)} \n",
        reply_markup=kb.kb_ch)
    await state.set_state(MainState.ch_profile)


@router.message(MainState.ch_name)
async def change_name(message: types.Message, state: FSMContext):
    user = await state.get_data()
    BotDB.update_name(message.chat.id, message.text)
    await message.answer(
        f"Отлично, проверьте ваши данные! \nИмя: {BotDB.get_name(message.chat.id)} \nВозраст: {BotDB.get_age(message.chat.id)} \nПол: {BotDB.get_sex(message.chat.id)} \nИнтересы: \n{BotDB.get_interests(message.chat.id)} \n",
        reply_markup=kb.kb_ch)
    await state.set_state(MainState.ch_profile)


@router.message(MainState.ch_sex)
async def change_sex(message: types.Message, state: FSMContext):
    user = await state.get_data()
    BotDB.update_sex(message.chat.id, message.text)
    await message.answer(
        f"Отлично, проверьте ваши данные! \nИмя: {BotDB.get_name(message.chat.id)} \nВозраст: {BotDB.get_age(message.chat.id)} \nПол: {BotDB.get_sex(message.chat.id)} \nИнтересы: \n{BotDB.get_interests(message.chat.id)} \n",
        reply_markup=kb.kb_ch)
    await state.set_state(MainState.ch_profile)


@router.message(MainState.ch_interest)
async def change_interest(message: types.Message, state: FSMContext):
    user = await state.get_data()
    try:
        user['interests']
    except:
        await state.update_data(interests=[])
        user = await state.get_data()

    if message.text in user['interests']:
        return await message.answer(f"Вы уже выбрали эту категорию, выберите еще {3 - len(user['interests'])}")
    elif message.text not in kb.cats_list:
        return await message.answer(f"Этой категории не существует, выберите из кнопок ниже:")
    elif len(user['interests']) < 3:
        await state.update_data(interests=user['interests'] + [message.text])
        user = await state.get_data()
    if len(user['interests']) == 3:
        BotDB.update_interests(message.chat.id, user['interests'][0], user['interests'][1], user['interests'][2])
    elif len(user['interests']) < 3:
        return await message.answer(f"{chr(10).join(user['interests'])}\n\nДобавлено, выберите ещё {3 - len(user['interests'])}")

    user = await state.get_data()
    await message.answer(
        f"Отлично, проверьте ваши данные! \nИмя: {BotDB.get_name(message.chat.id)} \nВозраст: {BotDB.get_age(message.chat.id)} \nПол: {BotDB.get_sex(message.chat.id)} \nИнтересы: \n{BotDB.get_interests(message.chat.id)} \n",
        reply_markup=kb.kb_ch)
    await state.set_state(MainState.ch_profile)