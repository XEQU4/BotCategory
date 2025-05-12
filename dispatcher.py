from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import TOKEN

# Initialize Bot instance with a default parse mode which will be passed to all API calls
bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher(storage=MemoryStorage())

# Creating a task scheduler
scheduler = AsyncIOScheduler()
url = 'sqlite:///database/tasks.sqlite'
scheduler.add_jobstore('sqlalchemy', url=url)
