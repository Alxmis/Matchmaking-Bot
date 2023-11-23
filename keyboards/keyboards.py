from aiogram import types

male = types.KeyboardButton(text = 'Мужчина')
female = types.KeyboardButton(text = 'Женщина')
kb_sex = types.ReplyKeyboardMarkup(keyboard = [[male, female],], resize_keyboard = True)

sex_ch = types.InlineKeyboardButton(text = 'Изменить пол')
name_ch = types.InlineKeyboardButton(text = 'Изменить имя')
age_ch = types.InlineKeyboardButton(text = 'Изменить возраст')

