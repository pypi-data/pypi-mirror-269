__all__ = [
    "setup_cache",
    "cache",
]

from datetime import timedelta
from functools import partial, wraps
from inspect import Parameter, signature
from typing import Any, Awaitable, Callable, ParamSpec, TypeVar, cast, get_type_hints

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
            *args: Any,
            **kwargs: Any,
        ) -> RT:
            storage = cast(AsyncCacheStorage, __request.app.state.cache_storage)
            key = f"{wrapper.__name__}:{str(__request.url)}"

            result = await storage.get(key)

            if not result:
                result = await route(*args, **kwargs)
                await storage.set(key, result, expires)

            return result

        _inject_request(wrapper)

        return wrapper

    return decorator


def _inject_request(wrapper: RouteType) -> None:
    hints = get_type_hints(wrapper)
    request_param = next(
        (name for name, hint in hints.items() if hint is Request),
        None,
    )
    if request_param:
        return

    request_param = "__request"
    setattr(
        wrapper,
        "__signature__",
        signature(wrapper).replace(
            parameters=[
                Parameter(
                    name=request_param,
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    annotation=Request,
                ),
            ]
            + list(signature(wrapper).parameters.values())
        ),
    )


async def _on_shutdown(app: FastAPI) -> None:
    storage = cast(AsyncCacheStorage, app.state.cache_storage)
    await storage.close()


def setup_cache(
    app: FastAPI,
    storage: AsyncCacheStorage,
    *,
    disconnect_on_shutdown: bool = True,
) -> None:
    app.state.cache_storage = storage

    if disconnect_on_shutdown:
        app.add_event_handler("shutdown", partial(_on_shutdown, app=app))
