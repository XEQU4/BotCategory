from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config import TEXT_CAPTION_CAR
from database.car_funcs import get_car, plus_views, get_car_contacts
from dispatcher import bot
from filters import IsClient
from handlers.admin_handlers.functions import create_media_group
from handlers.client_handlers.keyboards import IKB, RKB
from handlers.client_handlers.texts.get_text import get_client_text

router = Router()


@router.callback_query(F.data.startswith("car:"), IsClient())
async def car_info(query: CallbackQuery, state: FSMContext):
    car_id = query.data.split(":", 1)[1]
    user_id = query.message.chat.id

    data = await state.get_data()
    msgs = data['msgs'][:-1]
    last_msg = data['msgs'][-1]

    for msg in msgs:
        try:
            await bot.delete_message(chat_id=query.from_user.id,
                                     message_id=msg)

        except Exception:
            pass

    msgs = []

    car_data = await get_car(car_id)

    city = car_data[1]
    name = car_data[2]
    year = car_data[3]
    caption = car_data[5]
    medias: list = car_data[6]
    tags = car_data[7]
    country = car_data[11]

    media_group = await create_media_group(medias)
    text = TEXT_CAPTION_CAR.format(name, country, city, year, tags, caption)

    if len(media_group) > 10:
        one_group = []

        for media in media_group:
            one_group.append(media)

            if len(one_group) == 10:
                var1 = await bot.send_media_group(chat_id=user_id,
                                                  media=one_group)

                for msg in var1:
                    msgs.append(msg.message_id)

                one_group = []

        if one_group:
            var1 = await bot.send_media_group(chat_id=user_id,
                                              media=one_group)

            for msg in var1:
                msgs.append(msg.message_id)

    else:
        var1 = await bot.send_media_group(chat_id=user_id,
                                          media=media_group)

        for msg in var1:
            msgs.append(msg.message_id)

    var2 = await query.message.answer(text=text,
                                      reply_markup=await IKB.car_info(car_id))

    text = await get_client_text("car_info.py", "car_info")

    var3 = await query.message.answer(text=text,
                                      reply_markup=await RKB.car_info_back())

    msgs.append(var2.message_id)
    msgs.append(var3.message_id)

    try:
        await bot.delete_message(chat_id=query.from_user.id,
                                 message_id=last_msg)

    except Exception:
        pass

    await state.update_data(msgs=msgs)


@router.callback_query(F.data.startswith("carс:"), IsClient())
async def car_info2(query: CallbackQuery):
    car_id = query.data.split(":", 1)[1]

    car_data = await get_car(car_id)

    city = car_data[1]
    name = car_data[2]
    year = car_data[3]
    caption = car_data[5]
    tags = car_data[7]
    country = car_data[7]

    text = TEXT_CAPTION_CAR.format(name, country, city, year, tags, caption)

    await query.message.edit_text(text=text,
                                  reply_markup=await IKB.car_info(car_id))


@router.callback_query(F.data.startswith("contacts:"), IsClient())
async def car_contacts(query: CallbackQuery):
    car_id = query.data.split(":", 1)[1]

    contacts = await get_car_contacts(car_id)
    await plus_views(car_id)

    await query.message.edit_text(text=contacts,
                                  reply_markup=await IKB.car_contacts(car_id),
                                  disable_web_page_preview=True)
