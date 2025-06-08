from aiogram import types
from aiogram import BaseMiddleware
from collections import defaultdict
from aiogram import types
import time
import asyncio
from services.ban_storage import BanStorage


class MiddlewareAntiSpam(BaseMiddleware):
    def __init__(self, limit_interval=5, max_messages_per_interval=3, ban_time=60):
        self.limit_interval = limit_interval
        self.max_messages = max_messages_per_interval
        self.ban_time = ban_time
        self.user_message_times = defaultdict(list)
        self.ban_storage = BanStorage("storage/ban.json")
        
        super().__init__()

    async def __call__(self, handler, message: types.Message, data: dict):
        self.banned_users = await self.ban_storage._read_all()
        current_time = time.time()
        user_id = str(message.from_user.id)
        

        # Проверка бана
        if user_id in self.banned_users:
            if current_time < self.banned_users[user_id]:
                # Если забанен

                return await message.answer("Вы отправляете сообщения слишком часто. Пожалуйста, подождите.")    
            else:
                # Бан закончился
                del self.banned_users[user_id]
                self.user_message_times[user_id] = []
                await self.ban_storage._write_all(self.banned_users)

        # Очистка старых сообщений
        self.user_message_times[user_id] = [
            t for t in self.user_message_times[user_id] 
            if current_time - t < self.limit_interval
        ]

        # Добавление времени сообщения
        self.user_message_times[user_id].append(current_time)

        # Проверка лимита
        if len(self.user_message_times[user_id]) > self.max_messages:
            # Бан
            self.banned_users[user_id] = current_time + self.ban_time
            await self.ban_storage._write_all(self.banned_users)
            return await message.answer(
                f"Слишком много сообщений.\nПодождите {self.ban_time} секунд."
            )
        
        return await handler(message, data)
