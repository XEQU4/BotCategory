from typing import Union

from aiogram import Router
from aiogram.types import Message, CallbackQuery

from filters import IsClient

router = Router()


@router.message(IsClient())
async def handling_other_messages(message: Union[Message, CallbackQuery]):
    try:
        await message.delete()

    except Exception:
        try:
            await message.message.delete()

        except Exception:
            pass
