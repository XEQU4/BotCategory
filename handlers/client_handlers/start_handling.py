from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from FSM import FSMClient
from config import WELCOME_IMAGE_FOR_CLIENTS_PATH
from filters import IsClient
from handlers.client_handlers.functions import add_msg_ids, client_in_bot
from handlers.client_handlers.keyboards import IKB
from handlers.client_handlers.texts.get_text import get_client_text

router = Router()


@router.message(Command('start'), IsClient())
async def command_start_handling(message: Message, state: FSMContext):
    await state.clear()

    flag = await client_in_bot(state)
    if flag:
        return

    await state.set_state(FSMClient.passive)
    await state.update_data(f_index=0)
    await state.update_data(msgs=[])
    await state.update_data(tags=[])

    text = await get_client_text("start_handling.py", "command_start_handling")
    photo = FSInputFile(WELCOME_IMAGE_FOR_CLIENTS_PATH)

    var = await message.answer_photo(photo=photo,
                                     caption=text,
                                     reply_markup=await IKB.cmd_start())

    await add_msg_ids([var.message_id], state)


@router.message(F.text == "🔴", IsClient())
async def handling_other_messages(message: Message):
    try:
        await message.delete()

    except Exception:
        pass
