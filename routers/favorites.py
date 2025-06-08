from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import F
from services.favorites_storage import FavoritesStorage
from services.city_storage import Storage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.builders import main_keyboard

router = Router()

# Инициализируем хранилище
city_storage = Storage("storage/city.json")
storage = FavoritesStorage("storage/favorites.json")

# Работа с избранным
# Добавление в избранное
@router.message(Command("добавить <город>"))
async def cmd_add_fav(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply("Нужно написать название города:\n/добавить Стамбул", reply_markup=main_keyboard)

    city = parts[1].strip()
    await storage.add(message.from_user.id, city)
    await message.reply(f"Город {city} добавлен.", reply_markup=main_keyboard)

# Получение списка выбранных городов
@router.message(Command("избранное"))
async def cmd_list_fav(message: Message):
    favs = await storage.list(message.from_user.id)
    if not favs:
        return await message.reply("Нет избранного.", reply_markup=main_keyboard)
    text = "Ваше избранное:\n" + "\n".join(f"- {a}" for a in favs)
    # Кнопки для выбора каждого города
    kb = InlineKeyboardBuilder()
    for fav in favs:
        kb.button(text=f"Выбрать {fav}", callback_data=f"выбрать_город_{fav}", reply_markup=main_keyboard)
    kb.adjust(1)
    await message.reply(text, reply_markup=kb.as_markup())

# Выбрать по кнопке
@router.callback_query(lambda c: c.data.startswith("выбрать_город_"))
async def cmd_change_city(query: CallbackQuery):
    city = query.data.split("_", 2)[2]
    await city_storage.choice_city(query.from_user.id, city)
    await query.answer(f"Выбран {city}.", show_alert=False)

# Удаление из избранного
@router.message(Command("удалить <город>"))
async def cmd_remove_fav(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply("Вы забыли написать название города.\n/удалить Стамбул", reply_markup=main_keyboard)
    city = parts[1].strip()
    await storage.remove(message.from_user.id, city)
    await message.reply(f"❌ {city} удален из избранного.", reply_markup=main_keyboard)



