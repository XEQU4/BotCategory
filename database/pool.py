import asyncpg

from asyncpg import Pool

from config import DSN


class CreatePool:

    def __init__(self, dsn: str):
        """
        :param dsn: str - 'postgres://<user>:<password>@<host>:<port>/<database>'
        """
        self.config = dsn
        self._pool = None  # Pool object

    async def get_pool(self) -> Pool:
        """
        :return: Pool object
        """
        return self._pool

    async def create_pool(self) -> None:
        """
        Create and save the Pool object in the class CreatePool
        """
        self._pool = await asyncpg.create_pool(dsn=self.config)


db = CreatePool(DSN)  # DataBase Object
