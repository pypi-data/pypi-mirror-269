from redis import asyncio as aioredis


class BaseRedisStore:
    def __init__(
        self,
        protocol: str = "redis",
        host: str = "localhost",
        port: int = 6379,
        db_id: int = 0,
        min_pool_size: int = 5,
        max_pool_size: int = 10,
        **kwargs,
    ):
        """
        Give here the connection parameters to the redis. There is going to be
        a connection pool, so you can specify its size tool.

        Please note that this should be executed outside of an asyncio loop.

        :param host: IP/DNS host
        :param port: TCP port
        :param db_id: ID of the DB
        :param min_pool_size: minimum number of connections alive
        :param max_pool_size: maximum number of connections alive
        """
        # noinspection PyArgumentList
        super().__init__(**kwargs)

        self.protocol = protocol
        self.host = host
        self.port = port
        self.db_id = db_id
        self.min_pool_size = min_pool_size
        self.max_pool_size = max_pool_size
        self.redis = None

    async def async_init(self):
        """
        Handle here the asynchronous part of the init.
        """
        self.redis = await aioredis.from_url(
            f"{self.protocol}://{self.host}:{self.port}/{self.db_id}"
        )
