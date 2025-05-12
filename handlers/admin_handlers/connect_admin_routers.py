from aiogram import Dispatcher

from handlers.admin_handlers import start_handling, tags_settings, expiring, add_car, cars_settings


async def connect_admin(dp: Dispatcher):
    """Connect admin handlers router"""

    dp.include_router(start_handling.router)
    dp.include_router(tags_settings.router)
    dp.include_router(expiring.router)
    dp.include_router(add_car.router)
    dp.include_router(cars_settings.router)
