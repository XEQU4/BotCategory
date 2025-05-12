import sys

from database.pool import db
from logger.create_logger import logger
from asyncpg import exceptions


async def add_column_country():
    """This function is used only once at startup. It adds a 'country' column to the cars tables."""

    pool = await db.get_pool()

    query_1 = """
              ALTER TABLE active_car ADD country TEXT;
              UPDATE active_car SET country = 'UAE'
              """

    query_2 = """
              ALTER TABLE inactive_car ADD country TEXT;
              UPDATE inactive_car SET country = 'UAE'
              """

    query = """
            SELECT country FROM active_car
            """

    async with pool.acquire() as conn:
        try:
            async with conn.transaction():
                assert await conn.fetch(query)

        except Exception:
            pass

        else:
            return

    async with pool.acquire() as conn:
        try:
            async with conn.transaction():
                await conn.execute(query_1)
                await conn.execute(query_2)

        except Exception:
            pass


async def create_tables() -> None:
    """
    Create tables in the database for the car rental bot.
    """

    pool = await db.get_pool()

    async with pool.acquire() as conn:
        try:
            async with conn.transaction():
                query = """
                        CREATE TABLE IF NOT EXISTS active_car (
                            id TEXT PRIMARY KEY,
                            city TEXT,
                            name TEXT,
                            year TEXT,
                            services TEXT,
                            caption TEXT,
                            medias TEXT,
                            tags TEXT,
                            contacts TEXT,
                            days TEXT,
                            views TEXT,
                            country TEXT
                        )
                        """

                await conn.execute(query)

                query = """
                        CREATE TABLE IF NOT EXISTS inactive_car (
                            id TEXT PRIMARY KEY,
                            city TEXT,
                            name TEXT,
                            year TEXT,
                            services TEXT,
                            caption TEXT,
                            medias TEXT,
                            tags TEXT,
                            contacts TEXT,
                            days TEXT,
                            views TEXT,
                            country TEXT
                        )
                        """

                await conn.execute(query)

                query = """
                        CREATE TABLE IF NOT EXISTS main (
                            id VARCHAR (1),
                            tags TEXT,
                            act_inact VARCHAR (15)
                        )
                        """

                await conn.execute(query)

                query = """
                        SELECT * FROM main
                        """

                if await conn.fetchrow(query) is None:
                    query = """
                            INSERT INTO main (id) VALUES ('1')
                            """

                    await conn.execute(query)

        except exceptions.PostgresError as err:
            logger.critical(f"TABLES WERE NOT CREATED, BOT IS STOPPED! ERROR - {err}")
            sys.exit()

        else:
            logger.info("ALL TABLES SUCCESSFULLY CREATED IN DATABASE!")

    await add_column_country()
