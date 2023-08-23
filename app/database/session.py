import asyncpg


class Database:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self._pool = None
        self._connection = None

    async def connect(self):
        self._pool = await asyncpg.create_pool(self.dsn)

    async def disconnect(self):
        if self._pool:
            await self._pool.close()

    async def fetch(self, query: str):
        if not self._pool:
            await self.connect()
        self._connection = await self._pool.acquire()
        try:
            result = await self._connection.fetch(query)
            return result
        finally:
            await self._pool.release(self._connection)

    async def execute(self, query: str):
        if not self._pool:
            await self.connect()
        self._connection = await self._pool.acquire()
        try:
            result = await self._connection.execute(query)
            return result
        finally:
            await self._pool.release(self._connection)

