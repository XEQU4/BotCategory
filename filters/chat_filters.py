from typing import Union

from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from config import ADMIN_ID
from database.car_funcs import select_all_cars_ids


class IsAdmin(Filter):
    """Check if the user is an administrator."""

    async def __call__(self, query_or_message: Union[Message, CallbackQuery]) -> bool:
        chat_id = query_or_message.chat.id if isinstance(query_or_message, Message) else query_or_message.message.chat.id
        return chat_id == ADMIN_ID


class IsCar(Filter):
    """Check if the user is registered as a car (rental profile)."""

    async def __call__(self, query_or_message: Union[Message, CallbackQuery]) -> bool:
        cars_ids = await select_all_cars_ids()
        chat_id = query_or_message.chat.id if isinstance(query_or_message, Message) else query_or_message.message.chat.id
        return chat_id in cars_ids


class IsClient(Filter):
    """Check if the user is a regular client."""

    async def __call__(self, query_or_message: Union[Message, CallbackQuery]) -> bool:
        chat_id = query_or_message.chat.id if isinstance(query_or_message, Message) else query_or_message.message.chat.id

        return chat_id != ADMIN_ID and str(chat_id)[0] != "-"
