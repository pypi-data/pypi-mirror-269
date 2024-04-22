import pickle
from datetime import timedelta
from typing import Any, Sequence, cast

from redis import Redis
from redis.asyncio import Redis as AsyncRedis

from pythonic_cache.storage.base import AsyncCacheStorage, CacheStorage
from pythonic_cache.storage.utils import ensure_open


class RedisCacheStorage(CacheStorage):
    def __init__(self, redis: Redis) -> None:
        super().__init__()
        self._redis = redis

    @ensure_open
    def get(self, key: str) -> Any:
        value = self._redis.get(key)

        if not value:
            return None

        return pickle.loads(cast(bytes, value))

    @ensure_open
    def set(self, key: str, value: Any, expires: timedelta) -> None:
        self._redis.setex(key, expires, pickle.dumps(value))

    @ensure_open
    def delete(self, key: str) -> None:
        self._redis.delete(key)

    @ensure_open
    def clear(self) -> None:
        self._redis.flushall()

    @ensure_open
    def contains(self, key: str) -> bool:
        return len(cast(Sequence[str], self._redis.exists(key))) > 0

    @ensure_open
    def close(self) -> None:
        self._redis.close()
        self._closed = True


class AsyncRedisCacheStorage(AsyncCacheStorage):
    def __init__(self, redis: AsyncRedis) -> None:
        super().__init__()
        self._redis = redis

    @ensure_open
    async def get(self, key: str) -> Any:
        value = await self._redis.get(key)

        if not value:
            return None

        return pickle.loads(value)

    @ensure_open
    async def set(self, key: str, value: Any, expires: timedelta) -> Any:
        await self._redis.setex(key, expires, pickle.dumps(value))

    @ensure_open
    async def delete(self, key: str) -> None:
        await self._redis.delete(key)

    @ensure_open
    async def clear(self) -> None:
        await self._redis.flushall(asynchronous=True)

    @ensure_open
    async def contains(self, key: str) -> bool:
        return len(cast(Sequence[str], await self._redis.exists(key))) > 0

    @ensure_open
    async def close(self) -> None:
        await self._redis.aclose()
        self._closed = True
