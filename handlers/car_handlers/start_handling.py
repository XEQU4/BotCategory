# from typing import Union
#
# from aiogram import Router, F
# from aiogram.filters import Command
# from aiogram.fsm.context import FSMContext
# from aiogram.types import Message, CallbackQuery
#
# from dispatcher import bot
# from filters import IsCar
# from handlers.admin_handlers.keyboards import RKB
# from logger.create_logger import logger
#
# router = Router()
#
#
# @router.message(Command('start'), IsCar())
# async def command_start_handling(message: Message, state: FSMContext):
#     await message.delete()
#
#     text = f"Добрый день \- *{message.from_user.full_name}\!*"
#
#     await message.answer(text=text)
#
#
# @router.message(Command("cancel"), IsCar())
# @router.message(F.text == "Cancel", IsCar())
# @router.message(F.data == "cancel", IsCar())
# async def cancel(query_message: Union[Message, CallbackQuery], state: FSMContext):
#     chat_id = query_message.chat.id if isinstance(query_message, Message) else query_message.message.chat.id
#
#     try:
#         await query_message.delete() if isinstance(query_message, Message) else query_message.message.delete()
#
#     except Exception:
#         pass
#
#     current_state = await state.get_state()
#     if current_state is None:
#         return
#
#     try:
#         data = await state.get_data()
#         message_ids = data['msgs']
#
#         for msg_id in message_ids:
#             try:
#                 await bot.delete_message(chat_id=chat_id,
#                                          message_id=msg_id)
#
#             except Exception:
#                 pass
#
#     except Exception:
#         pass
#
#
#     logger.debug("CANCELLING STATE (CAR) - %r", current_state)
#     await state.clear()
#
#     await bot.send_message(chat_id=chat_id,
#                            text="_Отменено\._",
#                            reply_markup=await RKB.admin_start())