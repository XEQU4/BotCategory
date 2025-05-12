from aiogram import Dispatcher

from handlers.client_handlers import start_handling, other_messages, cities, tags, catalog, car_info


async def connect_client(dp: Dispatcher):
    """Connect client handlers router"""

    dp.include_router(start_handling.router)
    dp.include_router(cities.router)
    dp.include_router(tags.router)
    dp.include_router(catalog.router)
    dp.include_router(car_info.router)

    dp.include_router(other_messages.router)
