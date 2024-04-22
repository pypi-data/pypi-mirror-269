import httpx
import msgpack
import msgpack_numpy as m


class Client:
    def __init__(self, host):
        self.host = host

    def __getattr__(self, name):
        async def _func(*args, **kwargs):
            async with httpx.AsyncClient(timeout=httpx.Timeout(None)) as client:
                arguments = msgpack.packb([args, kwargs], default=m.encode)
                ret = await client.post(f"{self.host}/{name}", data=arguments)
                response = msgpack.unpackb(ret.content, object_hook=m.decode)
                return response

        return _func
