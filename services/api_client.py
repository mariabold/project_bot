import time
import aiohttp
from aiohttp import ClientError, ClientTimeout

class WeatherClient:
    def __init__(self, api_key_wheater: str, cache_ttl: int = 300, timeout: int = 10):
        self.api_key_wheater = api_key_wheater
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.timeout = timeout  # Таймаут запроса в секундах
        self._wheater_cache: dict[str, tuple[float, dict]] = {}  # city -> (timestamp, data)
        self.cache_ttl = cache_ttl  # Время жизни кэша в секундах


    async def get_weather(self, city: str) -> dict:
        now = time.time()
        if city in self._wheater_cache: # Проверка кэша
            ts, data = self._wheater_cache[city]
            if now - ts < self.cache_ttl:
                return data
        try:
            timeout = ClientTimeout(total=self.timeout) # Создаем клиент с таймаутом
            async with aiohttp.ClientSession(timeout=timeout) as session:
                try:
                    async with session.get(
                        f"{self.base_url}/weather?q={city}&appid={self.api_key_wheater}"
                    ) as response:
                        data = await response.json()
                        self._wheater_cache[city] = (now, data) # Сохраняем в кэш
                        return data
                        
                except ClientError as e:
                    raise Exception(f"Failed to get weather data: {str(e)}") # Обработка ошибок соединения/таймаута
                    
        except Exception as e:
            raise Exception(f"Unexpected error occurred: {str(e)}") # Обработка других исключений
