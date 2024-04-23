from datetime import timedelta
from functools import wraps
from typing import Any, Callable

from pythonic_cache.storage.base import AsyncCacheStorage, CacheStorage


class CacheClient:
    def __init__(self, storage: CacheStorage) -> None:
        self._storage = storage

    def cache(self, expires: timedelta = timedelta(hours=1)) -> Callable:
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                key = f"{func.__name__}:{str(args)}"

                result = self._storage.get(key)

                if not result:
                    result = func(*args, **kwargs)
                    self._storage.set(key, result, expires)

                return result

            return wrapper

        return decorator


class AsyncCacheClient:
    def __init__(self, storage: AsyncCacheStorage) -> None:
        self._storage = storage

    def cache(self, expires: timedelta = timedelta(hours=1)) -> Callable:
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                key = f"{func.__name__}:{str(args)}"

                result = await self._storage.get(key)

                if not result:
                    result = await func(*args, **kwargs)
                    await self._storage.set(key, result, expires)

                return result

            return wrapper

        return decorator
