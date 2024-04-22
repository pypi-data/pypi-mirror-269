__all__ = [
    "CacheStorage",
    "AsyncCacheStorage",
]

from abc import abstractmethod
from datetime import timedelta
from threading import Lock
from typing import Any


class Singleton(type):
    _instances: dict = {}
    __shared_instance_lock__: Lock = Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            with cls.__shared_instance_lock__:
                cls._instances[cls] = super().__call__(*args, **kwargs)

        return cls._instances[cls]


class CacheStorage(metaclass=Singleton):
    def __init__(self) -> None:
        self._closed = False

    @abstractmethod
    def get(self, key: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def set(self, key: str, value: Any, expires: timedelta) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def contains(self, key: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError


class AsyncCacheStorage(metaclass=Singleton):
    def __init__(self) -> None:
        self._closed = False

    @abstractmethod
    async def get(self, key: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def set(self, key: str, value: Any, expires: timedelta) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def clear(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def contains(self, key: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError
