from typing import Union

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import CITIES
from database.car_funcs import get_cars_main_photo_and_id_from_db_city_tags, get_car
from dispatcher import bot
from filters import IsClient
from handlers.client_handlers.functions import set_f_and_l_car_indexes, check_count_car
from handlers.client_handlers.keyboards import IKB, RKB
from handlers.client_handlers.texts.get_text import get_client_text

router = Router()


@router.callback_query(F.data == "search", IsClient())
@router.callback_query(F.data.in_(CITIES), IsClient())
@router.message(F.text == "⬅️", IsClient())
@router.message(lambda message: message.text in ["◀️", "▶️", "🔴"], IsClient())
async def catalog1(query_message: Union[Message, CallbackQuery], state: FSMContext):
    data = await state.get_data()

    if isinstance(query_message, Message) and query_message in ["◀️", "▶️", "🔴"]:
        await query_message.delete()

    if isinstance(query_message, CallbackQuery) and query_message.data in CITIES:
        await state.update_data(city=query_message.data)

        city = query_message.data

    else:
        if not data.get('city', False):
            return

        city = data['city']

        try:
            await query_message.delete()

        except Exception:
            pass

    country = data['country']

    await state.update_data(old_index=0)

    try:
        tags = data['tags']

    except Exception:
        tags = []

    try:
        cars_main_photos_and_ids = data['all_cars']

    except Exception:
        cars_main_photos_and_ids = await get_cars_main_photo_and_id_from_db_city_tags(country, city, tags)

    else:
        if not cars_main_photos_and_ids:
            cars_main_photos_and_ids = await get_cars_main_photo_and_id_from_db_city_tags(country, city, tags)

    mmpai = await get_cars_main_photo_and_id_from_db_city_tags(country, city, tags)  # Получем список моделей из бд, что бы в следующих циклах его нормализовать.

    for car in cars_main_photos_and_ids:
        if car not in mmpai:
            cars_main_photos_and_ids.remove(car)
            break

    for car in mmpai:
        if car not in cars_main_photos_and_ids:
            cars_main_photos_and_ids.append(car)
            break

    await state.update_data(all_cars=cars_main_photos_and_ids)

    count = len(cars_main_photos_and_ids)

    flag = await check_count_car(query_message, count, data)

    if flag:
        return

    user_id = query_message.from_user.id

    try:
        first_index = data["f_index"]

    except Exception:
        first_index = 0

    first_index, last_index = await set_f_and_l_car_indexes(query_message, count, first_index)

    if last_index > count:
        last_index = count
        first_index = 0 if count <= 0 else last_index - 5 if count % 5 == 0 else last_index - (count % 5)

    text_count = f"{last_index}/{count}"

    cars_data = cars_main_photos_and_ids[first_index:last_index]

    msgs = data["msgs"][:-1]
    last_msg = data["msgs"][-1]

    for msg_id in msgs:
        try:
            await bot.delete_message(chat_id=user_id,
                                     message_id=msg_id)

        except Exception:
            pass

    msgs = []

    for md in cars_data:
        main_photo: str = md[0]
        car = await get_car(md[1])
        services = car[4]
        tags = car[7]

        var = await bot.send_photo(chat_id=user_id,
                                   photo=main_photo,
                                   caption=f"{services}\n\n{tags}",
                                   reply_markup=await IKB.catalog_info(md[1]))

        msgs.append(var.message_id)

    text = (await get_client_text("catalog.py", "catalog")).format(text_count)

    if isinstance(query_message, CallbackQuery):
        var = await query_message.message.answer(text=text,
                                                 parse_mode=ParseMode.HTML,
                                                 reply_markup=await RKB.catalog(text_count))

    else:
        var = await query_message.answer(text=text,
                                         parse_mode=ParseMode.HTML,
                                         reply_markup=await RKB.catalog(text_count))

    msgs.append(var.message_id)

    try:
        await bot.delete_message(chat_id=user_id,
                                 message_id=last_msg)

    except Exception:
        pass

    await state.update_data(f_index=last_index)
    await state.update_data(msgs=msgs)