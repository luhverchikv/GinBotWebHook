from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup
)


start_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Сегодня'), KeyboardButton(text='Календарь')],
    [KeyboardButton(text='ИМТ'), KeyboardButton(text='СКФ')],
    [KeyboardButton(text='О Ферретаб')]
],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder='Сделай выбор')


sex_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Мужской')],
    [KeyboardButton(text='Женский')]
],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Выберите пол')


kreat_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='мг/дл')],
    [KeyboardButton(text='мкмоль/л')]
],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='мг/дл или мкмоль/л')
