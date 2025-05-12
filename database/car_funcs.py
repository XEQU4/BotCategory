from datetime import datetime, timedelta
from typing import Union, Any
from random import shuffle

from database.main import get_current_table
from database.pool import db
from database.car_active_inactive import move_to_inactive, move_to_active
from handlers.scheduler import delete_job, start_car_db_scheduler, add_car_to_inactive_table
from logger.create_logger import logger


async def select_all_cars_ids() -> list[int]:
    """
    Select all car IDs.

    :return: cars_ids - list[int]
    """
    queries = [
        """
        SELECT id FROM active_car
        """,
        """
        SELECT id FROM inactive_car
        """
    ]

    pool = await db.get_pool()

    async with pool.acquire() as conn:
        records1 = await conn.fetch(queries[0])
        records2 = await conn.fetch(queries[1])

    cars_ids = list(map(lambda id_: int(id_[0]), records1)) + list(map(lambda id_: int(id_[0]), records2))

    return cars_ids


async def get_car_name(car_id: Union[int, str]) -> str:
    """
    Select car name from 'active_car'.

    :param car_id: int | str - car telegram id
    """
    query = """
            SELECT name FROM active_car WHERE id = $1
            """

    pool = await db.get_pool()

    async with pool.acquire() as conn:
        record = await conn.fetchval(query, str(car_id))

    car_name = str(record)

    return car_name


async def get_expiring_cars_names_ids() -> [[str, int]]:
    """
    Select all cars names and ids whose subscription is expiring.

    :return: cars names and ids - list[list[str, int]]
    """
    query = """
            SELECT name, id, days FROM active_car
            """

    pool = await db.get_pool()

    async with pool.acquire() as conn:
        records = await conn.fetch(query)

    try:
        cars = list(map(lambda car_: list(car_), records))
    except Exception:
        return []
    else:
        if not cars or not cars[0]:
            return []

    today = datetime.now()

    exp_cars = []

    for car in cars:
        date_time_str = car[-1]
        date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')

        if int(str(date_time_obj - today).split()[0]) <= 3:
            exp_cars.append(car)

    return exp_cars


async def get_car_contacts(car_id: Union[int, str]) -> str:
    """
    Select car contacts from 'active_car'.

    :param car_id: int | str - car telegram id
    """
    query = """
            SELECT contacts FROM active_car WHERE id = $1
            """

    pool = await db.get_pool()

    async with pool.acquire() as conn:
        record = await conn.fetchval(query, str(car_id))

    contacts = str(record)

    return contacts


async def add_car_to_db(car_id: Union[int, str],
                        country: str,
                        city: str,
                        name: str,
                        year: str,
                        services: str,
                        caption: str,
                        medias: list[str],
                        tags: list[str],
                        contacts: str,
                        days: Union[str, None] = None) -> None:
    """
    Add a new car to 'active_car'.
    """
    if days is None:
        new_days = str(datetime.now() + timedelta(days=30))
    else:
        new_days = str(datetime.now() + timedelta(days=round(float(days))))

    new_medias = ",".join(medias)
    views = "0"
    new_tags = "#".join(tags)

    query = """
            INSERT INTO active_car VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
            """

    pool = await db.get_pool()

    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(
                query, str(car_id), city, name, str(year), services, caption, new_medias, new_tags, contacts, str(new_days), views, country)

    logger.info("[DATABASE] A NEW CAR ADDED TO THE DATABASE - ID: %s", car_id)


async def set_car(car_id: Union[int, str],
                  country: str,
                  city: str,
                  name: str,
                  year: str,
                  services: str,
                  caption: str,
                  medias: list[str],
                  tags: list[str],
                  contacts: str,
                  days: str) -> None:
    """
    Update or move car between tables, and update car data.

    :param car_id: car telegram id
    :param country: car country
    :param city: car city
    :param name: car name
    :param year: year of manufacture
    :param services: rental services and prices
    :param caption: car description
    :param medias: car medias (main_photo, photos and videos)
    :param tags: car tags
    :param contacts: contact information
    :param days: rental subscription days
    """
    pool = await db.get_pool()

    async with pool.acquire() as conn:
        try:
            query = """
                    SELECT * FROM active_car WHERE id = $1
                    """
            assert (await conn.fetchrow(query, car_id))[2]
        except Exception:
            table = "inactive_car"
        else:
            table = "active_car"

    if str(days)[0] == "-" and table == "active_car":
        await move_to_inactive(str(car_id))
        await delete_job(str(car_id))
        await add_car_to_inactive_table(str(car_id), round(float(days)))
        table = "inactive_car"

    elif str(days)[0] != "-" and table == "inactive_car":
        await move_to_active(str(car_id))
        await delete_job(str(car_id))
        await start_car_db_scheduler(str(car_id), round(float(days)))
        table = "active_car"

    else:
        if table == "active_car":
            await delete_job(str(car_id))
            await start_car_db_scheduler(str(car_id), round(float(days)))
        else:
            await delete_job(str(car_id))
            await add_car_to_inactive_table(str(car_id), round(float(days)))

    query = f"""
            UPDATE {table} 
            SET city = $1, name = $2, year = $3, services = $4, caption = $5, medias = $6, tags = $7, contacts = $8, days = $9, country = $11
            WHERE id = $10
            """

    new_tags = "#".join(tags)
    new_medias = ",".join(medias)
    new_days = str(datetime.now() + timedelta(days=round(float(days))))

    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(query, city, name, str(year), services, caption, new_medias, new_tags, contacts, str(new_days), str(car_id), country)

    logger.info("[DATABASE] CAR DATA UPDATED - ID: %s", car_id)


async def parse_medias(medias: str) -> dict:
    """
    medias: "main_photo:main_photo_id,photo:photo1_id,photo:photo2_id,video:video1_id,video:video2_id"

    :return: dict - {"main_photo": "main_photo_id", "photo": ["photo1_id", "photo2_id"], "video": ["video1_id", "video2_id"]}
    """
    medias_dict = dict()

    photos = []
    videos = []

    for media in medias.split(","):

        if media.split(":", 1)[0] == "main_photo":
            medias_dict.update(main_photo=media.split(":", 1)[1])

        elif media.split(":", 1)[0] == "photo":
            photos.append(media.split(":", 1)[1])

        elif media.split(":", 1)[0] == "video":
            videos.append(media.split(":", 1)[1])

    medias_dict.update(photo=photos)
    medias_dict.update(video=videos)

    return medias_dict


async def get_cars_main_photo_and_id_from_db() -> list[list[str, str]]:
    """
    Get the main photo and car IDs of the current table.

    :return: cars' main photo and id - [['car1_mphoto', 'car1_id'], ['car2_mphoto', 'car2_id'], ..., ['carn_mphoto', 'carn_id']]
    """
    table = await get_current_table()

    query = f"""
            SELECT medias, id FROM {table}
            """

    pool = await db.get_pool()

    async with pool.acquire() as conn:
        records = await conn.fetch(query)

    cars = []

    if records:
        for car in records:
            main_photo = (await parse_medias(str(car[0])))['main_photo']
            user_id = car[1]

            cars.append([main_photo, str(user_id)])

        shuffle(cars)

    return cars


async def get_car(car_id: Union[int, str]) -> list:
    """
    Get all car data where id = car_id.

    :returns: id [0] --- city [1] --- name [2] --- year [3] --- services [4] --- caption [5] --- medias [6] (list) --- tags [7] --- contacts [8] --- days [9] --- views [10] --- country [11]
    """
    table = await get_current_table()

    query = """
        SELECT * FROM {} WHERE id = $1
    """

    pool = await db.get_pool()

    async with pool.acquire() as conn:
        records = await conn.fetchrow(query.format(table), str(car_id))

    try:
        car = list(map(str, records))

    except TypeError:
        # If not found in active table, check inactive table
        if table == "active_car":
            table = "inactive_car"
        else:
            table = "active_car"

        async with pool.acquire() as conn:
            records = await conn.fetchrow(query.format(table), str(car_id))

        car = list(map(str, records))

    car[6]: str
    car[6] = car[6].split(",")
    car[7] = ",  ".join([f"<code>{tag}</code>" for tag in car[7].split("#")])
    car[9] = (str(datetime.strptime(car[9], '%Y-%m-%d %H:%M:%S.%f') - datetime.now())).split()[0]

    return car


async def set_car_days(days: int, car_id: int, flag: bool = True) -> None:
    """
    Set car subscription days and restart the scheduler.

    :param days: car subscription days
    :param car_id: car telegram id
    :param flag: move or not
    """
    table = await get_current_table()

    new_days = round(float(days))

    await delete_job(str(car_id))

    if table == "inactive_car" and flag:
        await move_to_active(str(car_id))
        table = "active_car"
        await start_car_db_scheduler(str(car_id), new_days)

    elif table == "active_car" and not flag:
        table = "inactive_car"
        await add_car_to_inactive_table(str(car_id), new_days)

    elif table == "active_car":
        await start_car_db_scheduler(str(car_id), new_days)

    elif table == "inactive_car":
        await add_car_to_inactive_table(str(car_id), new_days)

    new_days = datetime.now() + timedelta(days=new_days)

    query = f"""
            UPDATE {table} SET days = $1 WHERE id = $2
            """

    pool = await db.get_pool()

    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(query, str(new_days), str(car_id))

    logger.info("[DATABASE] CAR SUBSCRIPTION DAYS UPDATED - ID: %s", car_id)


async def del_car_from_db(car_id: Union[int, str]) -> None:
    """
    Delete car from the database and scheduler.

    :param car_id: car telegram id
    """
    await delete_job(car_id)

    query1 = """
             DELETE FROM active_car WHERE id = $1
             """

    query2 = """
             DELETE FROM inactive_car WHERE id = $1
             """

    pool = await db.get_pool()

    async with pool.acquire() as conn:
        try:
            async with conn.transaction():
                await conn.execute(query1, str(car_id))

        except Exception:
            async with conn.transaction():
                await conn.execute(query2, str(car_id))

    logger.info("[DATABASE] CAR (ID: %s) DELETED FROM DATABASE", car_id)


async def get_cars_main_photo_and_id_from_db_city_tags(country: str, city: str, tags: list[Union[str, Any]]) -> list[list[str, str]]:
    """
    Get the main photo and car IDs from the current table filtered by country, city, and tags.

    :param country: Car country
    :param city: Car city
    :param tags: Car tags list
    :return: cars main photo and id - [['car1_mphoto', 'car1_id'], ['car2_mphoto', 'car2_id'], ..., ['carn_mphoto', 'carn_id']]
    """
    query = """
            SELECT medias, id, tags FROM active_car WHERE city = $1 AND country = $2
            """

    pool = await db.get_pool()

    async with pool.acquire() as conn:
        records = await conn.fetch(query, city, country)

    cars = []

    if records:
        for car in records:
            main_photo = (await parse_medias(str(car[0])))['main_photo']
            user_id = car[1]
            tags_ = car[2].split("#")

            if tags and set(tags).issubset(tags_):
                cars.append([main_photo, str(user_id)])

            elif not tags:
                cars.append([main_photo, str(user_id)])

        if cars:
            shuffle(cars)

    return cars


async def plus_views(car_id: Union[int, str]) -> None:
    """
    Increase car profile views by +1.

    :param car_id: car Telegram id
    """
    queries = [
        """
        SELECT views FROM active_car WHERE id = $1
        """,
        """
        UPDATE active_car SET views = $1 WHERE id = $2
        """
    ]

    pool = await db.get_pool()

    async with pool.acquire() as conn:
        records = await conn.fetchval(queries[0], str(car_id))

    views = int(records) + 1

    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(queries[1], str(views), str(car_id))
