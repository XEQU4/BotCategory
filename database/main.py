from database.pool import db
from logger.create_logger import logger

"""------------------------------| act_inact |------------------------------"""


async def replacing_the_current_table(table: str) -> None:
    """
    Set table 'main' - act_inact (the current table where car data is updated)

    :param table: str ('active_car' or 'inactive_car')
    """
    query = """
            UPDATE main
            SET act_inact = $1
            WHERE id = $2
            """

    pool = await db.get_pool()

    async with pool.acquire() as conn:
        try:
            async with conn.transaction():
                await conn.execute(query, table, "1")

        finally:
            logger.info(f"[DATABASE] CAR DATA TABLE SWITCHED TO – '{table}'")


async def get_current_table() -> str:
    """
    Get from table 'main' - act_inact (the current table where car data is updated)

    :return: table name - str ('active_car' or 'inactive_car')
    """
    query = """
            SELECT act_inact FROM main
            """

    pool = await db.get_pool()

    async with pool.acquire() as conn:
        table = str(await conn.fetchval(query))

    return table


"""------------------------------| tags |------------------------------"""


async def get_tags() -> list[str]:
    """
    Get all tags from table 'main'

    :return: tags - list (['tag1', 'tag2', 'tag3', . . ., 'tagn'])
    """
    query = """
            SELECT tags FROM main
            """

    pool = await db.get_pool()

    async with pool.acquire() as conn:
        records = await conn.fetchval(query)

    if records:
        tags = [tag for tag in records.split("#") if tag and tag != ""]

        return tags

    return []


async def add_tag(tag: str) -> None:
    """
    Add a new tag to table 'main'

    :param tag: str
    """
    query = """
            UPDATE main SET tags = $1 WHERE id = '1'
            """

    tags: list[str] = await get_tags()
    tags.append(tag)
    tags: str = "#".join(tags)

    pool = await db.get_pool()

    async with pool.acquire() as conn:
        try:
            async with conn.transaction():
                await conn.execute(query, tags)

        finally:
            logger.info(f"[DATABASE] NEW TAG ADDED TO THE DATABASE – '{tag}'")


async def del_tag(tag: str) -> None:
    """
    Delete a tag from table 'main'

    :param tag: str
    """
    query = """
            UPDATE main SET tags = $1 WHERE id = '1'
            """

    tags: list[str] = await get_tags()
    tags.remove(tag)
    tags: str = "#".join(tags)

    pool = await db.get_pool()

    async with pool.acquire() as conn:
        try:
            async with conn.transaction():
                await conn.execute(query, tags)

        finally:
            logger.info(f"[DATABASE] TAG REMOVED FROM DATABASE – '{tag}'")
