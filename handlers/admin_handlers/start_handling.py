from typing import Union

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from dispatcher import bot
from filters import IsAdmin
from handlers.admin_handlers.keyboards import RKB
from logger.create_logger import logger

router = Router()

"""------------------------------| Command - start | Command - cmd |------------------------------"""


@router.message(Command('start'), IsAdmin())
async def command_start_handling(message: Message, state: FSMContext):
    await state.clear()

    text = f"Good day - <b>{message.from_user.full_name}</b> 👋\n\n" \
           f"You are the owner of this bot!\n" \
           f"\n" \
           f"You have access to these <b>text commands</b> below 👇, " \
           f"or you can use the <b>regular commands</b> located on the left (Menu) 👈"

    await message.answer(text=text,
                         reply_markup=await RKB.admin_start())


"""------------------------------| Command - cancel | Text - ❌ Cancel | Callback data - cancel |------------------------------"""


@router.message(Command("cancel"), IsAdmin())
@router.message(F.text == "❌ Cancel", IsAdmin())
@router.callback_query(F.data == "cancel", IsAdmin())
async def cancel(query_message: Union[Message, CallbackQuery], state: FSMContext):
    """
    Clear the state

    :param query_message: Message or CallbackQuery object
    :param state: FSM state
    :return: None
    """

    chat_id = query_message.chat.id if isinstance(query_message, Message) else query_message.message.chat.id

    current_state = await state.get_state()
    if current_state is None:
        return

    logger.debug("CANCELLING STATE (ADMIN) - %s", current_state)
    await state.clear()

    await bot.send_message(chat_id=chat_id,
                           text="<i>Cancelled.</i>",
                           reply_markup=await RKB.admin_start())
