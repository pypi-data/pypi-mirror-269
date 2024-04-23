from datetime import timedelta
from functools import wraps
from typing import Any, Callable, ParamSpec, TypeVar, cast

from flask import Flask, g, request

from pythonic_cache.storage.base import CacheStorage

P = ParamSpec("P")
RT = TypeVar("RT")

ViewType = Callable[P, RT]


def cache(expires: timedelta = timedelta(hours=1)) -> Callable[[ViewType], ViewType]:
    def decorator(view: ViewType) -> ViewType:
        @wraps(view)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> RT:  # type: ignore
            storage = cast(CacheStorage, g.__cache_storage)
            key = f"{wrapper.__name__}:{str(args)}:{request.url}"
            result = storage.get(key)
            if not result:
                result = view(*args, **kwargs)
                storage.set(key, result, expires)
            return result

        return wrapper

    return decorator


def _on_shutdown(*_: Any) -> None:
    if "__cache_storage" in g:
        g.__cache_storage.close()
        g.pop("__cache_storage")


def _inject_storage(storage: CacheStorage) -> None:
    if "__cache_storage" not in g:
        g.__cache_storage = storage


def setup_cache(
    app: Flask,
    cache_storage: CacheStorage,
    *,
    disconnect_on_shutdown: bool = True,
) -> None:
    if not isinstance(cache_storage, CacheStorage):
        raise TypeError("cache_storage must be an instance of CacheStorage")

    _inject_storage(cache_storage)

    if disconnect_on_shutdown:
        app.teardown_appcontext(_on_shutdown)
