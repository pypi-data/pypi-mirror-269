from datetime import timedelta
from functools import wraps
from inspect import Parameter, signature
from typing import Awaitable, Callable, ParamSpec, TypeVar, cast

from fastapi import FastAPI, Request

from pythonic_cache.storage.base import AsyncCacheStorage

P = ParamSpec("P")
RT = TypeVar("RT")
RouteType = Callable[P, Awaitable[RT]]


def cache(expires: timedelta = timedelta(hours=1)) -> Callable[[RouteType], RouteType]:
    def decorator(route: RouteType) -> RouteType:
        @wraps(route)
        async def wrapper(
            __request: Request,
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> RT:  # type: ignore
            storage = cast(AsyncCacheStorage, __request.app.state.cache_storage)
            key = f"{wrapper.__name__}:{str(args)}:{str(__request.url)}"
            result = await storage.get(key)
            if not result:
                result = await route(*args, **kwargs)
                await storage.set(key, result, expires)
            return result

        _inject_request(wrapper)
        return wrapper

    return decorator


def _inject_request(wrapper: RouteType) -> None:
    if Request not in wrapper.__annotations__.values():
        wrapper.__annotations__["__request"] = Request
        wrapper_signature = signature(wrapper).replace(
            parameters=[
                Parameter(
                    name="__request",
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    annotation=Request,
                ),
                *signature(wrapper).parameters.values(),
            ]
        )
        setattr(wrapper, "__signature__", wrapper_signature)


async def _on_shutdown(app: FastAPI) -> None:
    await app.state.cache_storage.close()


def setup_cache(
    app: FastAPI,
    storage: AsyncCacheStorage,
    *,
    disconnect_on_shutdown: bool = True,
) -> None:
    if not isinstance(storage, AsyncCacheStorage):
        raise TypeError("cache_storage must be an instance of AsyncCacheStorage")

    app.state.cache_storage = storage

    if disconnect_on_shutdown:
        app.add_event_handler("shutdown", lambda: _on_shutdown(app))
