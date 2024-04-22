import inspect
from typing import Callable

import msgpack
import msgpack_numpy as m
from caffeinism_utils.asyncio import run_in_threadpool
from fastapi import FastAPI, Request, Response


def ensure_awaitable(func, *args, **kwargs):
    if inspect.iscoroutinefunction(func):
        return func(*args, **kwargs)
    else:
        return run_in_threadpool(func, *args, **kwargs)


class Server(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def method(self, name: str):
        def decorator(func: Callable):
            @self.post(f"/{name}")
            async def _stub(request: Request):
                body = await request.body()
                args, kwargs = msgpack.unpackb(body, object_hook=m.decode)
                ret = await ensure_awaitable(func, *args, **kwargs)
                response = msgpack.packb(ret, default=m.encode)
                return Response(
                    content=response,
                    media_type="binary/octet-stream",
                    status_code=200,
                )

            return _stub

        return decorator
