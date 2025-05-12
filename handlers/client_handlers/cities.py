from typing import Union

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, CallbackQuery, Message

from config import CLIENT_CITIES_PATH, CLIENT_COUNTRIES_PATH, COUNTRIES_AND_CITIES
from dispatcher import bot
from filters import IsClient
from handlers.client_handlers.functions import add_msg_ids
from handlers.client_handlers.keyboards import IKB
from handlers.client_handlers.texts.get_text import get_client_text

router = Router()


@router.callback_query(F.data == "start", IsClient())
@router.message(F.text == "🌆 Change country", IsClient())
async def country(query_message: Union[CallbackQuery, Message], state: FSMContext):
    try:
        await query_message.message.delete()

    except Exception:
        try:
            await query_message.delete()

        except Exception:
            pass

    data = await state.get_data()
    msgs = data['msgs']

    await state.update_data(f_index=0)
    await state.update_data(all_cars=[])

    for msg in msgs:
        try:
            await bot.delete_message(chat_id=query_message.from_user.id,
                                     message_id=msg)

        except Exception:
            pass

    text = await get_client_text("cities.py", "country")
    photo = FSInputFile(CLIENT_COUNTRIES_PATH)

    if isinstance(query_message, CallbackQuery):
        var = await query_message.message.answer_photo(photo=photo,
                                                       caption=text,
                                                       reply_markup=await IKB.countries())

    else:
        var = await query_message.answer_photo(photo=photo,
                                               caption=text,
                                               reply_markup=await IKB.countries())

    await add_msg_ids([var.message_id], state)


@router.callback_query(lambda query: query.data in COUNTRIES_AND_CITIES.keys(), IsClient())
@router.message(F.text == "🏙 Change city", IsClient())
async def city(query_message: Union[CallbackQuery, Message], state: FSMContext):
    try:
        await query_message.message.delete()

    except Exception:
        try:
            await query_message.delete()

        except Exception:
            pass

    data = await state.get_data()
    msgs = data['msgs']

    await state.update_data(f_index=0)
    await state.update_data(all_cars=[])

    for msg in msgs:
        try:
            await bot.delete_message(chat_id=query_message.from_user.id,
                                     message_id=msg)

        except Exception:
            pass

    text = await get_client_text("cities.py", "city")
    photo = FSInputFile(CLIENT_CITIES_PATH)

    if isinstance(query_message, CallbackQuery):
        var = await query_message.message.answer_photo(photo=photo,
                                                       caption=text,
                                                       reply_markup=await IKB.cities(query_message.data))
        await state.update_data(country=query_message.data)

    else:
        ctry = data['country']
        var = await query_message.answer_photo(photo=photo,
                                               caption=text,
                                               reply_markup=await IKB.cities(ctry))

    await add_msg_ids([var.message_id], state)