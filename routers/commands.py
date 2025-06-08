from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import logging
from keyboards.builders import main_keyboard, start_keyboard


router = Router()

@router.message(Command("start"))
async def start_command_start(message: Message):
    await message.answer("Привет! Я бот, который поможет тебе узнать погоду\n"
                         "Введи /команды, чтобы узнать что я умею",
                         reply_markup=start_keyboard)

    logging.info(f"User {message.from_user.id} called /start")

@router.message(Command("команды"))
async def start_command_help(message: Message):
    await message.answer(
        "Команды:\n"
        "/start - запуск бота\n"
        "/погода - получить информацию о погоде\n"
        "/выбрать <город> - выбрать город\n"
        "/избранное - список городов в избранном\n"
        "/добавить <город> - добавить город в избранном\n"
        "/удалить <город> - удалить город в избранном\n"
        "/команды - перечень команд\n"
        "/поддержка - сообщить о проблеме",
        reply_markup=main_keyboard
    )
