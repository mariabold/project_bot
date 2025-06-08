from config.settings_bot import bot_config
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from routers import commands, open_weather_map, favorites, support, admin
from middlewares.throttling import MiddlewareAntiSpam
from utils import logger
import asyncio


async def main():
    bot = Bot(token=bot_config.telegram_api_key)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Регистрация роутеров
    dp.include_router(open_weather_map.router)
    dp.include_router(commands.router)
    dp.include_router(favorites.router)
    dp.include_router(support.router)
    dp.include_router(admin.router)

    # Подключение антиспама
    dp.message.middleware(MiddlewareAntiSpam())
    
    print("Bot is running...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


