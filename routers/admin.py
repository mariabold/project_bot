from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import logging
from keyboards.builders import main_keyboard, start_keyboard
from services.ban_storage import BanStorage
from services.city_storage import Storage
from filters.filters import IsAdmin
from aiogram import Bot
from config.settings_bot import bot_config

bot = Bot(token=bot_config.telegram_api_key)
router = Router()
ban_storage = BanStorage("storage/ban.json")
city_storage = Storage("storage/city.json")


# Запуск функционала админа
@router.message(IsAdmin(), Command("админ"))
async def admin_command_help(message: Message):
    await message.answer(
        "Команды:\n"
        "/бан <id> <минуты> - Бан пользователя\n"
        "/статистика - получить информацию о погоде\n"
        "/рассылка <сообщение> - разослать всем сообщение"
    )

# Бан пользователей
@router.message(IsAdmin(), Command("бан"))
async def admin_command_ban(message: Message):
    parts = message.text.split(maxsplit=2)
    user_id, minutes = int(parts[1].strip()), int(parts[2].strip())
    await ban_storage.ban_user(user_id, minutes)
    try:
        await bot.send_message(
            chat_id=int(user_id),
            text=f"Вы забанены на {minutes} минут."
        )
        await message.answer(f"Пользователь {user_id} забанен на {minutes} минут.")
    except:
        await message.answer(f"сообщение о бане не отправлено пользователю, возможно вы ошиблись в id")
    

    logging.info(f"User {user_id} baned.")

# Получение статистики
@router.message(IsAdmin(), Command("статистика"))
async def admin_command_stats(message: Message):
    users = await city_storage._read_all()
    await message.answer(f"Статистика\nКоличество пользователей: {len(users)}")

# Отправка сообщения пользователям
@router.message(IsAdmin(), Command("рассылка"))
async def admin_command_send(message: Message):
    send_text = message.text.split(maxsplit=1)[1].strip()
    users = await city_storage._read_all()
    for user_id in users:
        try:
            await bot.send_message(
                chat_id=int(user_id),
                text=send_text
            )
        except:
            pass
