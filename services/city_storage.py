import aiofiles
import asyncio
import json
from pathlib import Path
from typing import List, Dict

class Storage:
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        # Создаём папки, если их нет
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        # Внутри процесса блокировка, чтобы не читать/писать одновременно
        self._lock = asyncio.Lock()

    async def _read_all(self) -> Dict[str, List[str]]:
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

    async def get_city(self, user_id: int) -> List[str]:
        data = await self._read_all()
        city = data.get(str(user_id), "")
        return city

    async def choice_city(self, user_id: int, city: str):
        data = await self._read_all()
        data[str(user_id)] = city
        await self._write_all(data)

