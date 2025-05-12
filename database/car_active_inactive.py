from typing import Union

from database.pool import db
from logger.create_logger import logger

"""------------------------------| MOVING AND DELETE |------------------------------"""


async def move_to_inactive(car_id: Union[str, int]) -> None:
    """
    Move car from active to inactive table.

    :param car_id: int | str - car's Telegram ID
    """
    queries = [
        """
        SELECT *
        FROM active_car
        WHERE id = $1
        """,
        """
        DELETE
        FROM active_car
        WHERE id = $1
        """,
        """
        INSERT INTO inactive_car
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
        """
    ]

    pool = await db.get_pool()

    async with pool.acquire() as conn:
        car = await conn.fetchrow(queries[0], str(car_id))

        async with conn.transaction():
            await conn.execute(queries[1], str(car_id))
            await conn.execute(queries[2], *car)

    logger.info("[DATABASE] CAR (ID: %s) MOVED FROM 'active_car' TO 'inactive_car'", car_id)


async def delete_car_from_db(car_id: Union[str, int]) -> None:
    """
    Delete car from the database.

    :param car_id: int | str - car's Telegram ID
    """
    pool = await db.get_pool()

    async with pool.acquire() as conn:
        try:
            async with conn.transaction():
                query = """
                        DELETE
                        FROM inactive_car
                        WHERE id = $1
                        """
                await conn.execute(query, car_id)

        except Exception:
            async with conn.transaction():
                query = """
                        DELETE
                        FROM active_car
                        WHERE id = $1
                        """
                await conn.execute(query, car_id)

    logger.info("[DATABASE] CAR (ID: %s) DELETED FROM DATABASE", car_id)


async def move_to_active(car_id: Union[str, int]) -> None:
    """
    Move car from inactive to active table.

    :param car_id: int | str - car's Telegram ID
    """
    queries = [
        """
        SELECT *
        FROM inactive_car
        WHERE id = $1
        """,
        """
        DELETE
        FROM inactive_car
        WHERE id = $1
        """,
        """
        INSERT INTO active_car
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
        """
    ]

    pool = await db.get_pool()

    async with pool.acquire() as conn:
        car = await conn.fetchrow(queries[0], str(car_id))

        async with conn.transaction():
            await conn.execute(queries[1], str(car_id))
            await conn.execute(queries[2], *car)

    logger.info("[DATABASE] CAR (ID: %s) MOVED FROM 'inactive_car' TO 'active_car'", car_id)
