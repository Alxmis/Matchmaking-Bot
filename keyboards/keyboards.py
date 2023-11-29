from aiogram import types

male = types.KeyboardButton(text = 'Мужской')
female = types.KeyboardButton(text = 'Женский')
kb_sex = types.ReplyKeyboardMarkup(keyboard = [[male, female],], resize_keyboard = True)

sex_ch = types.KeyboardButton(text = 'Изменить пол')
name_ch = types.KeyboardButton(text = 'Изменить имя')
age_ch = types.KeyboardButton(text = 'Изменить возраст')
okay = types.KeyboardButton(text = 'Все окей!')
kb_ch = types.ReplyKeyboardMarkup(keyboard = [[sex_ch, age_ch, name_ch, okay]], resize_keyboard = True)

ch_profile = types.KeyboardButton(text = 'Изменить профиль')
search_conv = types.KeyboardButton(text = 'Найти собеседника')
kb_main = types.ReplyKeyboardMarkup(keyboard = [[ ch_profile, search_conv]], resize_keyboard = True)

kb_cancel = types.ReplyKeyboardMarkup(keyboard = [[types.KeyboardButton(text = 'Закончить сессию')]], resize_keyboard = True)