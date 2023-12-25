from aiogram import types

cats_list = 'Кино Спорт Туризм Музыка Еда Закончить'.split()

male = types.KeyboardButton(text='Мужской')
female = types.KeyboardButton(text='Женский')
kb_sex = types.ReplyKeyboardMarkup(keyboard=[[male, female], ], resize_keyboard=True)

sex_ch = types.KeyboardButton(text='Изменить пол')
name_ch = types.KeyboardButton(text='Изменить имя')
age_ch = types.KeyboardButton(text='Изменить возраст')
okay = types.KeyboardButton(text='Все окей!')
kb_ch = types.ReplyKeyboardMarkup(keyboard=[[sex_ch, age_ch, name_ch, okay]], resize_keyboard=True)

ch_profile = types.KeyboardButton(text='Изменить профиль')
search_conv = types.KeyboardButton(text='Найти собеседника')
delete_me = types.KeyboardButton(text='Удалить меня из бота')
kb_main = types.ReplyKeyboardMarkup(keyboard=[[ch_profile, search_conv, delete_me]], resize_keyboard=True)

kb_cancel = types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text='Закончить сессию')]], resize_keyboard=True)

cats = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text=cat) for cat in cats_list]
    ],
    resize_keyboard=True
)
