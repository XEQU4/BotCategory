import asyncio
import sys

from aiogram.types import BotCommand, BotCommandScopeChat

from config import ADMIN_ID
from database.create_tables import create_tables
from database.pool import db
from dispatcher import bot, dp, scheduler
from errors import error_handling
from handlers import connect_admin, connect_client
from logger.create_logger import init_logger, logger


async def main() -> None:
    # Initializing the Logger
    init_logger()

    # Initializing the database
    try:
        await db.create_pool()
        await create_tables()
    except BaseException as e:
        logger.critical("DATA BASE IS NOT CONNECTED, SO PROCESS WILL BE STOPPED!", e)
        raise e
    else:
        logger.info("DATA BASE IS SUCCESSFUL CONNECTED!")

    # Start the scheduler
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.critical("SCHEDULER IS NOT STARTED, SO PROCESS WILL BE STOPPED!")
        sys.exit()

    else:
        logger.info("SCHEDULER IS STARTED!")

    # Skipping all accumulated updates
    await bot.delete_webhook(drop_pending_updates=True)

    # Add default bot commands
    commands = [
        BotCommand(command="/add_car", description="Add a new car"),
        BotCommand(command="/set_cars", description="Manage car listings"),
        BotCommand(command="/set_tags", description="Manage car tags"),
        BotCommand(command="/exp_list", description="View expiring rentals"),
        BotCommand(command="/cmd", description="List of admin commands"),
        BotCommand(command="/cancel", description="Cancel the current action"),
    ]

    # for admin_id in ADMIN_IDS:
    await bot.set_my_commands(
        commands=commands, scope=BotCommandScopeChat(chat_id=ADMIN_ID)
    )

    logger.info("BOT COMMANDS ARE REGISTERED!")

    # Connecting routers to the dispatcher
    dp.include_routers(error_handling.router)

    await connect_admin(dp)
    # await connect_car(dp)
    await connect_client(dp)

    logger.info("ALL ROUTERS ARE CONNECTED!")

    # Run events dispatching
    logger.info("BOT IS STARTED!")

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())

    except (KeyboardInterrupt, SystemExit):
        logger.critical("BOT IS STOPPED!")
        sys.exit()

    except BaseException as ex:
        logger.critical(f"BOT IS STOPPED! ERROR: {ex}")
        raise ex
