from datetime import timedelta, datetime
from typing import Union

from apscheduler.jobstores.base import JobLookupError

from database.car_active_inactive import move_to_inactive, delete_car_from_db
from dispatcher import scheduler


async def start_car_db_scheduler(car_id: Union[int, str], days: int = 30):
    """
    Start car scheduler.
    """
    run_date = datetime.now() + timedelta(days=round(float(days)))  # Default: 1 month

    scheduler.add_job(add_car_to_inactive_table, "date", run_date=run_date, args=[car_id], id=str(car_id), replace_existing=True, coalesce=True)


async def add_car_to_inactive_table(car_id: Union[int, str], days: int = 30):
    """
    Move car from 'active_car' to 'inactive_car' and schedule deletion.
    """
    try:
        await move_to_inactive(car_id)

    except TypeError:
        pass

    run_date = datetime.now() + timedelta(days=abs(round(float(days))))  # Default: 2 months

    scheduler.add_job(delete_car, "date", run_date=run_date, args=[car_id], id=str(car_id), replace_existing=True, coalesce=True)


async def delete_car(car_id: Union[int | str]):
    """
    Delete car scheduler and delete car from database.
    """
    try:
        await delete_job(car_id)

    except Exception:
        pass

    await delete_car_from_db(car_id)


async def delete_job(car_id: Union[int, str]):
    """
    Delete car scheduler.
    """
    try:
        scheduler.remove_job(str(car_id))

    except JobLookupError:
        pass
