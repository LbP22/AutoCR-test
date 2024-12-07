from ..utils.singleton import Singleton
from ..utils.config import config, Environment
import aioredis


class RedEngine(metaclass=Singleton):
    def __init__(self, redis_url=config.REDIS_URL):
        self.redis_url = redis_url
        self.con = None

    async def get_con(self):
        if not self.con:
            self.con = await aioredis.create_redis_pool(self.redis_url)

        return self.con

    async def drop_db(self):
        if config.ENV not in [Environment.LOCAL, Environment.TEST]:
            print('You can not do this here.')
            return

        await (await self.get_con()).flushdb()

    async def get(self, *args, **kwargs) -> bytes:
        return await (await self.get_con()).get(*args, **kwargs)

    async def set(self, *args, **kwargs):
        return await (await self.get_con()).set(*args, **kwargs)
