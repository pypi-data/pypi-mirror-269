import orjson

from ..redis import BaseRedisStore
from .base import BaseContextStore, Context


class RedisContextStore(BaseRedisStore, BaseContextStore):
    """
    Store the context as a serialized JSON inside Redis. It's made to be
    compatible with the register storage, if using the same Redis DB.
    """

    async def _get(self, key: str) -> Context:
        try:
            return orjson.loads(await self.redis.get(key))
        except (ValueError, TypeError):
            return {}

    async def _set(self, key: str, data: Context) -> None:
        await self.redis.set(key, orjson.dumps(data), ex=self.ttl)
