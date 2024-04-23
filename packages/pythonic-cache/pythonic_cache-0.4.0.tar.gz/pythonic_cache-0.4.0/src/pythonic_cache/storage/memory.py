__all__ = [
    "MemoryCacheStorage",
    "AsyncMemoryCacheStorage",
]

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Generic, TypeVar

from pythonic_cache.storage.base import AsyncCacheStorage, CacheStorage
from pythonic_cache.storage.utils import ensure_open

T = TypeVar("T")


@dataclass(frozen=True)
class MemoryStorageValue(Generic[T]):
    value: T
    expires: datetime


class MemoryCacheStorage(CacheStorage):
    def __init__(self) -> None:
        super().__init__()
        self._cache: dict[str, MemoryStorageValue] = {}

    @ensure_open
    def get(self, key: str) -> Any:
        storage_value = self._cache.get(key)

        if not storage_value:
            return None

        if storage_value.expires < datetime.now():
            self.delete(key)
            return None

        return storage_value.value

    @ensure_open
    def set(self, key: str, value: Any, expires: timedelta) -> None:
        self._cache[key] = MemoryStorageValue(value, expires + datetime.now())

    @ensure_open
    def delete(self, key: str) -> None:
        self.contains(key) and self._cache.pop(key)

    @ensure_open
    def clear(self) -> None:
        self._cache.clear()

    @ensure_open
    def contains(self, key: str) -> bool:
        return key in self._cache

    @ensure_open
    def close(self) -> None:
        del self._cache
        self._closed = True


class AsyncMemoryCacheStorage(AsyncCacheStorage):
    def __init__(self) -> None:
        super().__init__()
        self._cache: dict[str, MemoryStorageValue] = {}

    @ensure_open
    async def get(self, key: str) -> Any:
        storage_value = self._cache.get(key)

        if not storage_value:
            return None

        if storage_value.expires < datetime.now():
            await self.delete(key)
            return None

        return storage_value.value

    @ensure_open
    async def set(self, key: str, value: Any, expires: timedelta) -> None:
        self._cache[key] = MemoryStorageValue(value, expires + datetime.now())

    @ensure_open
    async def delete(self, key: str) -> None:
        if await self.contains(key):
            del self._cache[key]

    @ensure_open
    async def clear(self) -> None:
        self._cache.clear()

    @ensure_open
    async def contains(self, key: str) -> bool:
        return key in self._cache

    @ensure_open
    async def close(self) -> None:
        del self._cache
        self._closed = True
