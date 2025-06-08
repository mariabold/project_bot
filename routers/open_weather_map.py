from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import F
from config.settings_open_weather_map import open_weather_map_config
from services.api_client import WeatherClient
from services.city_storage import Storage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime
from keyboards.builders import main_keyboard

router = Router()

city_storage = Storage("storage/city.json")
mal_client = WeatherClient(open_weather_map_config.open_weather_map_api_key)


# Команда выбора города
@router.message(Command("выбрать"))
async def cmd_choose(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply("Укажите название города \n/выбрать Стамбул", reply_markup=main_keyboard)

    city = parts[1].strip()
    await city_storage.choice_city(message.from_user.id, city)
    await message.reply(f"Город {city} выбран.")


# Команда получения данных о погоде по выбранному городу
@router.message(Command("погода"))
async def cmd_weather(message: Message):
    city = await city_storage.get_city(message.from_user.id)
    if city == "":
        await message.reply("Город не указан.\nНапишите /выбрать Стамбул", reply_markup=main_keyboard)
        return 
    response = await mal_client.get_weather(city)
    if response['cod'] == 200:
        return await message.reply(f"{response['name']}\n{response['weather'][0]['main']}\n\nТемпература {round(response['main']['temp'] -273, 1)} °С\nОщущается как {round(response['main']['feels_like'] -273, 1)} °С\nВетер {response['wind']['speed']} м/с", reply_markup=main_keyboard)
    else:
        return await message.reply(f"WRONG\n{response['cod']}\nmessage: {response['message']}", reply_markup=main_keyboard)
    
    
        
    
    
