from typing import Union

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile

from FSM import FSMAdmin
from config import TEXT_CAPTION_CAR, ADMIN_ID, COUNTRIES_AND_CITIES, SAMPLE_MEDIA_GROUP_PATH
from database.main import replacing_the_current_table, get_tags
from database.car_funcs import get_cars_main_photo_and_id_from_db, get_car, set_car_days, del_car_from_db, \
    set_car
from dispatcher import bot
from filters import IsAdmin
from handlers.admin_handlers.keyboards import IKB, RKB
from handlers.admin_handlers.functions import set_len_and_new_len, check_count_car, create_media_group, \
    check_car_set_datas
from logger.create_logger import logger

router = Router()

"""------------------------------SET CAR------------------------------"""


@router.message(F.text == "🛠 Manage cars", IsAdmin())
@router.message(Command("set_car"), IsAdmin())
async def command_set_car_handling(message: Message, state: FSMContext):
    await state.clear()

    text = "Which cars would you like to view or edit?"

    await message.answer(text=text,
                         reply_markup=await IKB.cars_act_inact(),
                         parse_mode=ParseMode.HTML)

    await state.set_state(FSMAdmin.carset1)

    await state.update_data(len_=0)
    await state.update_data(msgs=[])
    await state.update_data(table=False)
    await state.update_data(cars_main=[])


"""------------------------------CB: inact | CB: act | CB: bm------------------------------"""
"""------------------------------◀️ | ▶️------------------------------"""


@router.callback_query(FSMAdmin.carset1, lambda query: query.data in ["carset:inact", "carset:act", "carset:bm"],
                       IsAdmin())
@router.callback_query(FSMAdmin.carset3, lambda query: query.data == "carset:del_conf", IsAdmin())
@router.message(FSMAdmin.carset1, lambda message: message.text in ["◀️", "▶️", "⏪", "⏩"], IsAdmin())
async def cb_inact_act(query_message: Union[Message, CallbackQuery], state: FSMContext):
    data = await state.get_data()  # Получаем данные из FSM

    if isinstance(query_message, CallbackQuery) and query_message.data.split(":")[1] not in ["bm", "del_conf"]:
        if data['table']:  # Если кнопки Не активные и Активные один из них уже был нажат
            return  # Выходим из функции

        table = query_message.data.split(':')[1]  # В ином случае,
        await replacing_the_current_table(f"{table}ive_car")  # сохроняем нашу таблицу в базу данных
        await state.update_data(table=True)  # и в FSM

    elif isinstance(query_message, CallbackQuery) and query_message.data.split(":")[1] == "del_conf":
        text = "The car has been deleted!"

        await query_message.answer(text=text,
                                   cache_time=10,
                                   show_alert=True)

        car = data['car']
        name = car[2]
        car_id = car[0]

        text = f"<i>The car was deleted by user - <b>\"{query_message.from_user.full_name}\"</b></i>;\n\n" \
               f"Car model name: <b><code>{name}</code></b>;\n" \
               f"Car Telegram ID: <b><code>{car_id}</code></b>"

        # for admin_id in ADMIN_IDS:
        await bot.send_message(chat_id=ADMIN_ID,
                               text=text)

        data = await state.get_data()
        car = data['car']
        car_id = car[0]

        await del_car_from_db(car_id)

        logger.debug(f"CAR DELETED: car_name - {name} ; car_id - {car_id}")

        await state.set_state(FSMAdmin.carset1)

    if not data['cars_main']:  # Если мы ранее не сохроняли полученный список моделей из базы данных
        cars_main_photos_and_ids = await get_cars_main_photo_and_id_from_db()  # То получаем этот список из базы данных в хаотичном порядке

        await state.update_data(cars_main=cars_main_photos_and_ids)  # И сохраняем его в FSM

    else:
        cars_main_photos_and_ids = data['cars_main']  # В ином случае, получем его из FSM

    mmpai = await get_cars_main_photo_and_id_from_db()  # Получем список моделей из бд, что бы в следующих циклах нормализовать наш список

    for car in cars_main_photos_and_ids:
        if car not in mmpai:
            cars_main_photos_and_ids.remove(car)

            await state.update_data(cars_main=cars_main_photos_and_ids)
            break

    for car in mmpai:
        if car not in cars_main_photos_and_ids:
            cars_main_photos_and_ids.append(car)

            await state.update_data(cars_main=cars_main_photos_and_ids)
            break

    count = len(cars_main_photos_and_ids)  # Получаем количество моделей

    flag = await check_count_car(query_message, count, data)  # Фильтруем моделей

    if flag:
        return

    user_id = query_message.from_user.id
    len_ = data["len_"]  # Начальный индекс списка моделей из 5

    len_, new_len_ = await set_len_and_new_len(query_message, count,
                                               len_)  # Получаем конечный индекс списка моделей из 5 и меняем начальный если это потребуется

    if new_len_ > count:
        new_len_ = count
        len_ = 0 if count <= 0 else new_len_ - 5 if count % 5 == 0 else new_len_ - (count % 5)

    text_count = f"{new_len_}/{count}"
    cars_data = cars_main_photos_and_ids[len_:new_len_]  # Получем главное фото и ID выбранных пяти моделей

    msgs = data["msgs"]  # Список ID сообщений которых понадобится удалить для замены
    for msg_id in msgs:
        await bot.delete_message(chat_id=user_id,
                                 message_id=msg_id)

    await state.update_data(msgs=[])

    msgs = []

    # В цикле мы по очереди отправляем выбранных моделей, и сохраняем message_id каждого отправленного сообщения
    for md in cars_data:
        main_photo: str = md[0]
        car = await get_car(md[1])
        services = car[4]
        tags = car[7]

        var = await bot.send_photo(chat_id=user_id,
                                   photo=main_photo,
                                   caption=f"{services}\n\n{tags}",
                                   reply_markup=await IKB.car_info2(md[1]))

        msgs.append(var.message_id)

    text = f"<i>Number of cars: <b>{text_count}</b></i>"

    # Отправляем текст с Reply клавиатурой
    if isinstance(query_message, CallbackQuery):
        var = await query_message.message.answer(text=text,
                                                 parse_mode=ParseMode.HTML,
                                                 reply_markup=await RKB.cars_actinact(text_count))

    else:
        var = await query_message.answer(text=text,
                                         parse_mode=ParseMode.HTML,
                                         reply_markup=await RKB.cars_actinact(text_count))

    msgs.append(var.message_id)

    await state.update_data(len_=new_len_)
    await state.update_data(msgs=msgs)
    await state.update_data(car=None)


"""------------------------------| CallbackQuery - carset:<car_id> |------------------------------"""
"""------------------------------| Text - ✅ Confirm | Text - ⛔ Stop | Текст - ✅ Done |------------------------------"""


@router.callback_query(FSMAdmin.carset1,
                       lambda query: query.data.split(":")[0] == "carset" and query.data.split(":")[1] == "info",
                       IsAdmin())
@router.message(FSMAdmin.carset16, F.text.in_(["✅ Confirm", "⛔ Stop", "✅ Done"]), IsAdmin())
@router.message(FSMAdmin.carset3, F.text.in_(["✅ Done"]), IsAdmin())
@router.message(FSMAdmin.carset4, F.text.in_(["✅ Done"]), IsAdmin())
@router.message(FSMAdmin.carset5, F.text.in_(["✅ Done"]), IsAdmin())
@router.message(FSMAdmin.carset6, F.text.in_(["✅ Done"]), IsAdmin())
@router.message(FSMAdmin.carset7, F.text.in_(["✅ Done"]), IsAdmin())
@router.message(FSMAdmin.carset8, F.text.in_(["✅ Done"]), IsAdmin())
@router.message(FSMAdmin.carset9, F.text.in_(["✅ Done"]), IsAdmin())
@router.message(FSMAdmin.carset10, F.text.in_(["✅ Done"]), IsAdmin())
@router.message(FSMAdmin.carset11, F.text.in_(["✅ Done"]), IsAdmin())
@router.message(FSMAdmin.carset12, F.text.in_(["✅ Done"]), IsAdmin())
@router.message(FSMAdmin.carset13, F.text.in_(["✅ Done"]), IsAdmin())
@router.message(FSMAdmin.carset14, F.text.in_(["✅ Done"]), IsAdmin())
@router.message(FSMAdmin.carset15, F.text.in_(["✅ Done"]), IsAdmin())
async def cb_carset_car_id(query: Union[CallbackQuery, Message], state: FSMContext):
    if isinstance(query, Message) and query.text == "✅ Confirm":
        data = await state.get_data()

        car_id = data['car'][0]
        country = data['set_country']
        city = data['set_city']
        name = data['set_name']
        year = data['set_year']
        services = data['set_services']
        caption = data['set_caption']
        medias = data['set_media']
        tags = data['set_tags']
        contacts = data['set_contacts']
        days = data['set_days']

        await set_car(car_id, country, city, name, year, services, caption, medias, tags, contacts, days)

        text = f"<i>Car data was updated by user - <b>\"{query.from_user.full_name}\"</b></i>;\n\n" \
               f"Car model name: <b><code>{name}</code></b>;\n" \
               f"Car Telegram ID: <b><code>{car_id}</code></b>"

        # for admin_id in ADMIN_IDS:
        await bot.send_message(chat_id=ADMIN_ID,
                               text=text)

        logger.debug(f"CAR DATA CHANGED: car_name - {name} ; car_id - {car_id}")

        await state.set_state(FSMAdmin.carset1)

    elif isinstance(query, Message) and query.text == "✅ Done":
        data = await state.get_data()
        flag = await check_car_set_datas(state)

        if flag:
            car_id = data['car'][0]
            car = await get_car(car_id)

            try:
                name = data['set_name']
            except Exception:
                name = car[2]

            text = f"<i>Car data was updated by user - <b>\"{query.from_user.full_name}\"</b></i>;\n\n" \
                   f"Car model name: <b><code>{name}</code></b>;\n" \
                   f"Car Telegram ID: <b><code>{car_id}</code></b>"

            # for admin_id in ADMIN_IDS:
            await bot.send_message(chat_id=ADMIN_ID,
                                   text=text)

            logger.debug(f"CAR DATA CHANGED: car_name - {name} ; car_id - {car_id}")

        await state.set_state(FSMAdmin.carset1)

    elif isinstance(query, Message) and query.text == "⏭ Skip":
        await state.set_state(FSMAdmin.carset1)

    user_id = query.from_user.id

    data = await state.get_data()

    if isinstance(query, CallbackQuery):
        car_id = query.data.split(":")[-1]

    else:
        car_id = data['car'][0]

    car = await get_car(car_id)
    city = car[1]
    name = car[2]
    year = car[3]
    caption = car[5]
    medias: list = car[6]
    tags = car[7]
    contacts = car[8]
    days = int(car[9])
    views = car[10]
    country = car[11]

    msgs = data["msgs"]  # Список ID сообщений которых понадобится удалить для замены
    for msg_id in msgs:
        try:
            await bot.delete_message(chat_id=user_id,
                                     message_id=msg_id)

        except Exception:
            pass

    await state.update_data(msgs=[])
    msgs = []

    await state.update_data(car=car)

    media_group = await create_media_group(medias)
    text = TEXT_CAPTION_CAR.format(name, country, city, year, tags, caption) + f"\nCONTACTS:  {contacts}"

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

    if isinstance(query, CallbackQuery):
        var2 = await query.message.answer(text=text,
                                          reply_markup=await IKB.car_data_set(views, days))

    else:
        var2 = await query.answer(text=text,
                                  reply_markup=await IKB.car_data_set(views, days))

    msgs.append(var2.message_id)

    await state.update_data(msgs=msgs)


"""------------------------------CB: carset:days------------------------------"""


@router.callback_query(FSMAdmin.carset1, lambda query: query.data == "carset:days", IsAdmin())
async def cb_carset_days(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    try:
        car = data['car']
    except Exception:
        return

    days = int(car[9])

    await query.message.edit_reply_markup(reply_markup=await IKB.car_days_set(days))

    text = "<i><b>PS: If the number is greater than zero, the car will stay active for that many days before moving to the inactive list.\n" \
           "If the number is negative, it will be treated as a positive number, and the car will immediately move to the inactive list. " \
           "After the inactive period, the car's data will be deleted automatically!</b></i>"

    var = await query.message.answer(text=text)

    msgs = data['msgs']
    msgs.append(var.message_id)
    await state.update_data(msgs=msgs)

    await state.set_state(FSMAdmin.carset2)


@router.callback_query(FSMAdmin.carset2,
                       lambda query: query.data.split(":")[0:2] == ["carset", "days"] and query.data.split(":")[2] in "-*/+", IsAdmin())
async def cb_carset_days2(query: CallbackQuery):
    data = query.data.split(":")
    days = int(data[-1])

    await bot.answer_callback_query(callback_query_id=query.id)

    if data[-2] == "*":
        if days != 0:
            days *= 2
    elif data[-2] == "/":
        if days != 0:
            days /= 2
    elif data[-2] == "+":
        days += 1
    elif data[-2] == "-":
        days -= 1

    try:
        await query.message.edit_reply_markup(reply_markup=await IKB.car_days_set(int(days)))
    except Exception:
        pass


@router.callback_query(FSMAdmin.carset2, lambda query: query.data == "carset:inline_bd", IsAdmin())
@router.callback_query(FSMAdmin.carset3, lambda query: query.data == "carset:inline_bd", IsAdmin())
async def cb_carset_bd(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    car = data['car']
    days = int(car[9])
    views = car[10]

    await query.message.edit_reply_markup(reply_markup=await IKB.car_data_set(views, days))
    await state.set_state(FSMAdmin.carset1)


@router.callback_query(FSMAdmin.carset2, lambda query: query.data.split(":")[0:3] == ["carset", "days", "save"], IsAdmin())
@router.callback_query(FSMAdmin.carset2, lambda query: query.data.split(":")[0:3] == ["carset", "days", "transfer"], IsAdmin())
async def cb_carset_days3(query: CallbackQuery, state: FSMContext):
    data = query.data.split(":")
    days = int(data[-1])

    if days in [-1, 0, 1]:
        return await query.answer(
            text="The number of days cannot be -1, 0, or 1!",
            show_alert=True,
            cache_time=3
        )

    if days <= 0 and query.data.split(":")[2] == "save":
        await query.message.edit_reply_markup(reply_markup=await IKB.car_days_set(int(days), "transfer"))

        return await bot.answer_callback_query(callback_query_id=query.id,
                                               text="Since the number is negative, if there is any remaining subscription time, the car will move to the inactive list. Click again to confirm.",
                                               show_alert=True,
                                               cache_time=12)

    data = await state.get_data()
    car = data['car']
    views = car[10]
    name = car[2]
    car_id = car[0]

    if days > 0:
        await set_car_days(days, car[0])
    else:
        await set_car_days(days, car[0], False)

    car = await get_car(car[0])
    await state.update_data(car=car.copy())

    await query.message.edit_reply_markup(reply_markup=await IKB.car_data_set(views, days))

    await bot.answer_callback_query(callback_query_id=query.id,
                                    text="Subscription days have been updated!",
                                    show_alert=True)

    logger.debug(f"CAR SUBSCRIPTION DAYS UPDATED: car_name - {name} ; car_id - {car_id} ; new_days - {days}")

    await state.set_state(FSMAdmin.carset1)
    return None


"""------------------------------CB: carset:del_car------------------------------"""


@router.callback_query(FSMAdmin.carset1, lambda query: query.data == "carset:del_car", IsAdmin())
async def cb_carset_del_car(query: CallbackQuery, state: FSMContext):
    text = "Are you sure you want to delete this car and all its associated data?"

    await query.answer(text=text, cache_time=10, show_alert=True)
    await query.message.edit_reply_markup(reply_markup=await IKB.del_car())

    await state.set_state(FSMAdmin.carset3)


"""------------------------------CB: carset:set------------------------------"""


@router.callback_query(FSMAdmin.carset1, lambda query: query.data == "carset:set", IsAdmin())
async def cb_carset_set(query: CallbackQuery, state: FSMContext):
    text = "<b>You are about to edit car information</b>. You will need to provide the following data or skip fields as needed:\n\n" \
           "1. Country\n" \
           "2. City\n" \
           "3. Car Name\n" \
           "4. Year of Manufacture\n" \
           "5. Short Description for Catalog\n" \
           "6. Full Description for Profile\n" \
           "7. Photos\n" \
           "8. Main Photo\n" \
           "9. Videos\n" \
           "10. Tags\n" \
           "11. Contact Information"

    await query.message.answer(text=text)

    count = 0
    countries = ""

    for country in COUNTRIES_AND_CITIES.keys():
        countries += f"\n{count + 1}.  <code>{country}</code>"
        count += 1

    text = f"<i>Please select a country from the list:</i>\n{countries}"
    await query.message.answer(text=text, reply_markup=await RKB.country_can2())

    await state.set_state(FSMAdmin.carset4)


"""------------------------------COUNTRY > CITY------------------------------"""


@router.message(FSMAdmin.carset4, IsAdmin())
async def carset20(message: Message, state: FSMContext):
    if message.text is None:
        return await message.answer(
            text="<b><i>No text detected! Please select a country from the list.</i></b>",
            reply_markup=await RKB.country_can2()
        )

    country = message.text

    if message.text == "⏭ Skip":
        data = await state.get_data()
        car = data['car']
        country = car[11]

    elif country not in COUNTRIES_AND_CITIES.keys():
        return await message.answer(
            text="<b><i>Please select a country from the list!</i></b>",
            reply_markup=await RKB.country_can2()
        )

    await state.update_data(set_country=country)
    await state.set_state(FSMAdmin.carset5)

    count = 0
    cities = ""

    for city in COUNTRIES_AND_CITIES[country]:
        cities += f"\n{count + 1}.  <code>{city}</code>"
        count += 1

    text = f"<i>Please select a city from the list:</i>\n{cities}"
    await message.answer(text=text, reply_markup=await RKB.city_can2(country))
    return None


"""------------------------------CITY > NAME------------------------------"""


@router.message(FSMAdmin.carset5, IsAdmin())
async def carset4(message: Message, state: FSMContext):
    data = await state.get_data()
    country = data['set_country']

    if message.text is None:
        return await message.answer(
            text="<b><i>No text detected! Please select a city from the list.</i></b>",
            reply_markup=await RKB.city_can2(country)
        )

    city = message.text

    if message.text == "⏭ Skip":
        car = data['car']
        city = car[1]

    elif city not in COUNTRIES_AND_CITIES[country]:
        return await message.answer(
            text="<b><i>Please select a city from the list!</i></b>",
            reply_markup=await RKB.city_can2(country)
        )

    await state.update_data(set_city=city)
    await state.set_state(FSMAdmin.carset6)

    text = "<i>Please enter the car's name:</i>"
    await message.answer(text=text, reply_markup=await RKB.skip())
    return None


"""------------------------------NAME > YEAR------------------------------"""


@router.message(FSMAdmin.carset6, IsAdmin())
async def carset5(message: Message, state: FSMContext):
    if message.text is None:
        return await message.answer(
            text="<b><i>No text detected! Please enter the car name or skip.</i></b>",
            reply_markup=await RKB.skip()
        )

    name = message.text

    if message.text == "⏭ Skip":
        data = await state.get_data()
        car = data['car']
        name = car[2]

    await state.update_data(set_name=name)
    await state.set_state(FSMAdmin.carset7)

    text = "<i>Please enter the year of manufacture:</i>"
    await message.answer(text=text, reply_markup=await RKB.skip())
    return None


"""------------------------------YEAR > SERVICES------------------------------"""


@router.message(FSMAdmin.carset7, IsAdmin())
async def carset6(message: Message, state: FSMContext):
    if message.text is None:
        return await message.answer(
            text="<b><i>No text detected! Please enter the year of manufacture or skip.</i></b>",
            reply_markup=await RKB.skip()
        )

    year = message.text

    if message.text == "⏭ Skip":
        data = await state.get_data()
        car = data['car']
        year = car[3]

    elif not message.text.isdigit() or str(message.text)[0] == "-":
        return await message.answer(
            text="<b><i>Please send a valid positive number!</i></b>",
            reply_markup=await RKB.skip()
        )

    await state.update_data(set_year=year)
    await state.set_state(FSMAdmin.carset8)

    text = "<i>Please write a short description for the catalog:</i>"
    await message.answer(text=text, reply_markup=await RKB.skip())
    return None


"""------------------------------SERVICES > CAPTION------------------------------"""


@router.message(FSMAdmin.carset8, IsAdmin())
async def carset7(message: Message, state: FSMContext):
    if message.text is None:
        return await message.answer(
            text="<b><i>No text detected! Please write a short description or skip.</i></b>",
            reply_markup=await RKB.skip()
        )

    services = message.text

    if message.text == "⏭ Skip":
        data = await state.get_data()
        car = data['car']
        services = car[4]

    await state.update_data(set_services=services)
    await state.set_state(FSMAdmin.carset9)

    text = "<i>Please write a full description for the car profile:</i>"
    await message.answer(text=text, reply_markup=await RKB.skip())
    return None


"""------------------------------CAPTION > PHOTOS------------------------------"""


@router.message(FSMAdmin.carset9, IsAdmin())
async def carset8(message: Message, state: FSMContext):
    if message.text is None:
        return await message.answer(
            text="<b><i>No text detected! Please write a full description or skip.</i></b>",
            reply_markup=await RKB.can_fin()
        )

    caption = message.text

    if message.text == "⏭ Skip":
        data = await state.get_data()
        car = data['car']
        caption = car[5]

    await state.update_data(set_caption=caption)
    await state.update_data(set_media=[])
    await state.set_state(FSMAdmin.carset10)

    text = "<i>Send a media group of photos or individual photos. When you finish uploading, click <b>\"➡️ Continue\"</b>.\n" \
           "If you don't want to update photos, click <b>\"➡️ Skip\"</b>:</i>"

    photo = FSInputFile(SAMPLE_MEDIA_GROUP_PATH)
    await bot.send_photo(chat_id=message.chat.id,
                         caption=text,
                         photo=photo,
                         reply_markup=await RKB.can_next2())
    return None


"""------------------------------PHOTOS > MAIN PHOTO------------------------------"""


@router.message(FSMAdmin.carset10, IsAdmin())
async def carset9(message: Message, state: FSMContext):
    if message.text == "➡️ Continue":
        data = await state.get_data()
        media = data['set_media']

        if not media:
            return await message.answer(
                text="<b><i>No photos uploaded yet!</i></b>",
                reply_markup=await RKB.can_next2()
            )

        await state.set_state(FSMAdmin.carset11)

        text = "<i>Please send the main photo that will appear in the catalog:</i>"
        return await message.answer(text=text, reply_markup=await RKB.skip())

    elif message.text == "⏭ Skip":
        data = await state.get_data()
        medias = data['car'][6]
        media = [md for md in medias if md.split(":")[0] == "photo"]

        await state.update_data(set_media=media)
        await state.set_state(FSMAdmin.carset11)

        text = "<i>Please send the main photo that will appear in the catalog:</i>"
        return await message.answer(text=text, reply_markup=await RKB.skip())

    if not message.photo:
        return await message.answer(
            text="<b><i>This is not a photo!</i></b>",
            reply_markup=await RKB.skip()
        )

    data = await state.get_data()
    media = data['set_media']
    media.append(f"photo:{message.photo[0].file_id}")

    await state.update_data(set_media=media)
    return None


"""------------------------------MAIN PHOTO > VIDEOS------------------------------"""


@router.message(FSMAdmin.carset11, IsAdmin())
async def carset10(message: Message, state: FSMContext):
    if message.text == "⏭ Skip" and state:
        text = "<i>Send a media group of videos or send them individually. If you don't want to update the videos, click <b>\"⏭ Skip\"</b>:</i>"
        await message.answer(text=text, reply_markup=await RKB.can_next2())

        data = await state.get_data()
        media = data['set_media']
        medias = data['car'][6]

        for md in medias:
            if md.split(":")[0] == "main_photo":
                media.append(md)
                break

        await state.update_data(set_media=media)
        await state.set_state(FSMAdmin.carset12)
        return None

    elif not message.photo:
        return await message.answer(text="<b><i>No media detected!</i></b>", reply_markup=await RKB.skip())

    else:
        if await state.get_state() != FSMAdmin.carset12:
            text = "<i>Send a media group of videos or send them individually. If you don't want to update the videos, click <b>\"➡️ Skip\"</b>:</i>"
            await message.answer(text=text, reply_markup=await RKB.can_next2())

            data = await state.get_data()
            media = data['set_media']
            media.append(f"main_photo:{message.photo[0].file_id}")

            await state.update_data(set_media=media)
            await state.set_state(FSMAdmin.carset12)
    return None


"""------------------------------VIDEOS > TAGS------------------------------"""


@router.message(FSMAdmin.carset12, IsAdmin())
async def carset11(message: Message, state: FSMContext):
    if message.photo:
        return await message.answer(text="<b><i>This is not a video!</i></b>", reply_markup=await RKB.can_next2())

    if not message.video and message.text not in ["⏭ Skip", "➡️ Continue", "✅ Confirm"]:
        return await message.answer(text="<b><i>No media detected!</i></b>", reply_markup=await RKB.can_next2())

    data = await state.get_data()

    if message.text in ["⏭ Skip", "➡️ Continue", "✅ Confirm"]:
        if message.text == "➡️ Continue":
            for media in data['set_media']:
                if media.split(":")[0] == "video":
                    break
            else:
                return await message.answer(
                    text="<b><i>You haven't uploaded any videos yet. Confirm skipping video upload?</i></b>",
                    reply_markup=await RKB.skip_can()
                )

        elif message.text == "⏭ Skip":
            media = data['set_media']
            medias = data['car'][6]

            for md in medias:
                if md.split(":")[0] == "video":
                    media.append(md)

            await state.update_data(set_media=media)

        tags = await get_tags()

        await state.set_state(FSMAdmin.carset13)

        text = "<i>Select tags from the list below. Selected tags:</i>\n" + "\n-  " + "\n-  ".join(
            data['car'][7].split(",  ")
        )

        car_tags = [tag.rstrip("</code>").lstrip("</code>") for tag in data['car'][7].split(",  ")]
        await state.update_data(set_tags=car_tags)

        return await message.answer(text=text, reply_markup=await IKB.tags(tags, data['car'][0]))

    media = data['set_media']
    media.append(f"video:{message.video.file_id}")

    await state.update_data(set_media=media)
    return None


"""------------------------------TAGS > CONTACTS------------------------------"""


@router.callback_query(FSMAdmin.carset13, lambda query: query.data.split(":")[0] == "addtag", IsAdmin())
async def carset12(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    user_id = data['car'][0]

    if query.data.split(":")[-1] != user_id:
        return None

    if query.data.split(":")[1] == "add":
        tags = data['set_tags']

        if not tags:
            return await query.message.answer(text="<b><i>You haven't selected any tags!</i></b>")

        await state.set_state(FSMAdmin.carset14)
        await query.message.edit_reply_markup(reply_markup=None)

        text = "<i>Please enter the contact information:</i>"
        await query.message.answer(text=text, reply_markup=await RKB.skip())
        return None

    tag = ":".join(query.data.split(":")[1:-1])

    text_tags = list(map(lambda tag_: tag_.split("-  ", 1)[1], query.message.text.split("\n")[2:]))

    tags = data['set_tags']
    tags_db = await get_tags()

    if tag not in tags:
        text = query.message.html_text
        await query.message.edit_text(text=f"{text}\n-  <code>{tag}</code>", reply_markup=await IKB.tags(tags_db, data['car'][0]))

        tags.append(tag)

    else:
        index = int(text_tags.index(tag)) + 2
        text = query.message.html_text.split("\n")
        text.pop(index)
        text = "\n".join(text)

        await query.message.edit_text(text=text, reply_markup=await IKB.tags(tags_db, data['car'][0]))

        tags.remove(tag)

    await state.update_data(set_tags=tags)
    return None


"""------------------------------CONTACTS > DAYS------------------------------"""


@router.message(FSMAdmin.carset14, IsAdmin())
async def carset13(message: Message, state: FSMContext):
    contacts = message.text

    if message.text and message.text == "⏭ Skip":
        data = await state.get_data()
        car = data['car']
        contacts = car[8]

    elif message.text is None:
        return await message.answer(text="<b><i>No text detected!</i></b>", reply_markup=await RKB.skip())

    await state.update_data(set_contacts=contacts)

    text = "<i><b>PS:</b> If the number is positive, the car will stay in the active catalog for that many days. " \
           "If the number is negative (e.g., -30), it will stay inactive for 30 days and then be completely deleted.</i>"
    await message.answer(text=text)

    text = "<i>How many days should the car remain active or inactive?</i>"
    await message.answer(text=text, reply_markup=await RKB.skip())

    await state.set_state(FSMAdmin.carset15)
    return None


"""------------------------------DAYS > CALLBACKS------------------------------"""


@router.message(FSMAdmin.carset15, IsAdmin())
async def carset14(message: Message, state: FSMContext):
    if message.text is None:
        return await message.answer(
            text="<b><i>No text detected!</i></b>",
            reply_markup=await RKB.skip()
        )

    if message.text[0] == "-":
        try:
            days = "".join(message.text.split()).strip()
        except Exception:
            return await message.answer(
                text="<b><i>Please send a valid number!</i></b>",
                reply_markup=await RKB.skip()
            )

        if not days[1:].isdigit():
            return await message.answer(
                text="<b><i>Please send a valid number!</i></b>",
                reply_markup=await RKB.skip()
            )

    elif not message.text.isdigit() and message.text != "⏭ Skip":
        return await message.answer(
            text="<b><i>Please send a valid number!</i></b>",
            reply_markup=await RKB.skip()
        )

    else:
        days = message.text.strip()

    if days == "⏭ Skip":
        data = await state.get_data()
        car = data['car']
        days = car[9]

    await state.update_data(set_days=days)

    data = await state.get_data()

    medias = data['set_media']
    main_photo = ""

    for media in medias:
        if media.split(":")[0] == "main_photo":
            main_photo = media.split(":", 1)[1]
            break

    await bot.send_photo(
        chat_id=message.chat.id,
        photo=main_photo,
        reply_markup=await IKB.car_info(data['car'][0])
    )

    text = "<i>Please review and confirm updating the car information or cancel.\n" \
           "(<b>Cancel | Confirm</b>)</i>"
    await message.answer(text=text, reply_markup=await RKB.con_can2())

    await state.set_state(FSMAdmin.carset16)
    return None


"""------------------------------CALLBACKS > CONFIRM------------------------------"""


@router.callback_query(FSMAdmin.carset16, lambda query: query.data.split(":")[0] == "addcar", IsAdmin())
async def carset15(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    user_id = data['car'][0]

    if query.data.split(":")[-1] != user_id:
        return

    if query.data.split(":")[1] == "info":
        data = await state.get_data()

        city = data['set_city']
        name = data['set_name']
        year = data['set_year']
        caption = data['set_caption']
        medias = data['set_media']
        country = data['set_country']

        tags = ",  ".join([f"<code>{tag}</code>" for tag in data['set_tags']])

        media_group = await create_media_group(medias)
        text = TEXT_CAPTION_CAR.format(name, country, city, year, tags, caption)

        msgs = []

        if len(media_group) > 10:
            one_group = []

            for media in media_group:
                one_group.append(media)

                if len(one_group) == 10:
                    var1 = await bot.send_media_group(chat_id=query.message.chat.id, media=one_group)

                    for msg in var1:
                        msgs.append(msg.message_id)

                    one_group = []

            if one_group:
                var1 = await bot.send_media_group(chat_id=query.message.chat.id, media=one_group)

                for msg in var1:
                    msgs.append(msg.message_id)

        else:
            var1 = await bot.send_media_group(chat_id=query.message.chat.id, media=media_group)

            for msg in var1:
                msgs.append(msg.message_id)

        var2 = await query.message.answer(
            text=text,
            reply_markup=await IKB.car_back_contacts(data['car'][0])
        )

        await query.message.delete()

        msgs.append(var2.message_id)

        await state.update_data(msgs=msgs)

    elif query.data.split(":")[1] == "backinfo":
        data = await state.get_data()

        medias = data['set_media']
        main_photo = [media.split(":", 1)[1] for media in medias if media.split(":", 1)[0] == "main_photo"][0]

        message_ids = data['msgs']

        for message_id in message_ids:
            try:
                await bot.delete_message(chat_id=query.message.chat.id, message_id=message_id)
            except Exception:
                pass

        await bot.send_photo(
            chat_id=query.message.chat.id,
            photo=main_photo,
            reply_markup=await IKB.car_info(data['car'][0])
        )

    elif query.data.split(":")[1] == "contacts":
        data = await state.get_data()

        message_ids = data['msgs']

        for message_id in message_ids:
            try:
                await bot.delete_message(chat_id=query.message.chat.id, message_id=message_id)
            except Exception:
                pass

        contacts = data['set_contacts']

        await bot.send_message(
            chat_id=query.message.chat.id,
            text=contacts,
            reply_markup=await IKB.car_back_to_info(data['car'][0]),
            disable_web_page_preview=True
        )
