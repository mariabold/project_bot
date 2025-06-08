from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_kb = [
        [KeyboardButton(text="/команды")],
    ]
start_keyboard = ReplyKeyboardMarkup(keyboard=start_kb,
                               resize_keyboard=True,
                               one_time_keyboard=True)
        
main_kb = [
        [KeyboardButton(text="/погода")],
        [KeyboardButton(text="/поддержка"), KeyboardButton(text="/избранное")],
    ]
main_keyboard = ReplyKeyboardMarkup(keyboard=main_kb,
                               resize_keyboard=True,
                               one_time_keyboard=False)

