import aiofiles
import asyncio
import json
from pathlib import Path
from typing import List, Dict

class FavoritesStorage:
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        # Внутри процесса блокировка
        self._lock = asyncio.Lock()

    async def _read_all(self) -> Dict[str, List[str]]:
        """Прочитать весь JSON `{user_id: [city, ...]}`."""
        async with self._lock:
            if not self.filepath.exists():
                return {}
            async with aiofiles.open(self.filepath, 'r', encoding='utf-8') as f:
                text = await f.read()
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    return {}

    async def _write_all(self, data: Dict[str, List[str]]):
        """Записать весь словарь в файл."""
        async with self._lock:
            async with aiofiles.open(self.filepath, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(data, ensure_ascii=False, indent=2))

    async def list(self, user_id: int) -> List[str]:
        data = await self._read_all()
        return data.get(str(user_id), [])

    async def add(self, user_id: int, city: str):
        data = await self._read_all()
        user_key = str(user_id)
        user_list = set(data.get(user_key, []))
        user_list.add(city)
        data[user_key] = list(user_list)
        await self._write_all(data)

    async def remove(self, user_id: int, city: str):
        data = await self._read_all()
        user_key = str(user_id)
        user_list = set(data.get(user_key, []))
        if city in user_list:
            user_list.remove(city)
            data[user_key] = list(user_list)
            await self._write_all(data)
