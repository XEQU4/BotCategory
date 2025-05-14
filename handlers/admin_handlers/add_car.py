from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile

from FSM import FSMAdmin
from config import COUNTRIES_AND_CITIES, TEXT_CAPTION_CAR, ADMIN_ID, SAMPLE_MEDIA_GROUP_PATH
from database.car_funcs import select_all_cars_ids, add_car_to_db
from database.main import get_tags
from dispatcher import bot
from filters import IsAdmin
from handlers.admin_handlers.functions import create_media_group
from handlers.admin_handlers.keyboards import IKB, RKB
from handlers.scheduler import start_car_db_scheduler
from logger.create_logger import logger

router = Router()

"""------------------------------ADD CAR------------------------------"""


@router.message(F.text == "➕ Add car", IsAdmin())
@router.message(Command("add_car"), IsAdmin())
async def command_add_car_handling(message: Message, state: FSMContext):
    await state.clear()

    text = "<b>You are about to manually add a car to the rental catalog.</b>\n\n" \
           "You will need to provide the following information:\n\n" \
           "1. Telegram ID\n" \
           "2. Country\n" \
           "3. City\n" \
           "4. Car model name\n" \
           "5. Year of manufacture\n" \
           "6. Short description (for catalog listing)\n" \
           "7. Full description (for detailed profile)\n" \
           "8. Photos\n" \
           "9. Main photo\n" \
           "10. Video (optional, can skip)\n" \
           "11. Tags (for filtering)\n" \
           "12. Contact details\n\n" \
           "First, <i>please send the Telegram ID of the car profile</i>.\n\n" \
           "You can get the ID using this bot: https://t.me/username_to_id_bot"

    await message.answer(text=text,
                         reply_markup=await RKB.can())

    await state.set_state(FSMAdmin.addcar0)


"""------------------------------ID > COUNTRY------------------------------"""


@router.message(FSMAdmin.addcar0, IsAdmin())
async def addcar0(message: Message, state: FSMContext):
    if message.text is None:
        return await message.answer(
            text="<b><i>No text detected! Please send the ID as text.</i></b>",
            reply_markup=await RKB.can()
        )

    if not message.text.isdigit() or str(message.text)[0] == "-":
        return await message.answer(
            text="<b><i>Please send a valid numeric ID!</i></b>",
            reply_markup=await RKB.can()
        )

    if int(message.text) in await select_all_cars_ids():
        return await message.answer(
            text="<b><i>A car with this ID already exists in the database!</i></b>",
            reply_markup=await RKB.can()
        )

    await state.update_data(car_id=message.text)
    await state.set_state(FSMAdmin.addcar1)

    countries_list = ""
    for idx, country in enumerate(COUNTRIES_AND_CITIES.keys(), start=1):
        countries_list += f"\n{idx}.  <code>{country}</code>"

    text = f"<i>Please select a country from the list:</i>\n{countries_list}"
    await message.answer(text=text, reply_markup=await RKB.country_can())
    return None


"""------------------------------COUNTRY > CITY------------------------------"""


@router.message(FSMAdmin.addcar1, IsAdmin())
async def addcar1(message: Message, state: FSMContext):
    if message.text is None:
        return await message.answer(
            text="<b><i>No text detected! Please select a country.</i></b>",
            reply_markup=await RKB.country_can()
        )

    if message.text not in COUNTRIES_AND_CITIES.keys():
        return await message.answer(
            text="<b><i>Please select a valid country from the list!</i></b>",
            reply_markup=await RKB.country_can()
        )

    await state.update_data(country=message.text)
    await state.set_state(FSMAdmin.addcar2)

    country = message.text
    cities_list = ""
    for idx, city in enumerate(COUNTRIES_AND_CITIES[country], start=1):
        cities_list += f"\n{idx}.  <code>{city}</code>"

    text = f"<i>Please select a city from the list:</i>\n{cities_list}"
    await message.answer(text=text, reply_markup=await RKB.city_can(country))
    return None


"""------------------------------CITY > NAME------------------------------"""


@router.message(FSMAdmin.addcar2, IsAdmin())
async def addcar2(message: Message, state: FSMContext):
    data = await state.get_data()
    country = data['country']

    if message.text is None:
        return await message.answer(
            text="<b><i>No text detected! Please select a city.</i></b>",
            reply_markup=await RKB.city_can(country)
        )

    if message.text not in COUNTRIES_AND_CITIES[country]:
        return await message.answer(
            text="<b><i>Please select a valid city from the list!</i></b>",
            reply_markup=await RKB.city_can(country)
        )

    await state.update_data(city=message.text)
    await state.set_state(FSMAdmin.addcar3)

    text = "<i>Please send the car model name:</i>"
    await message.answer(text=text, reply_markup=await RKB.can())
    return None


"""------------------------------NAME > YEAR------------------------------"""


@router.message(FSMAdmin.addcar3, IsAdmin())
async def addcar3(message: Message, state: FSMContext):
    if message.text is None:
        return await message.answer(
            text="<b><i>No text detected! Please send the car model name.</i></b>",
            reply_markup=await RKB.can()
        )

    if "<" in message.text or ">" in message.text:
        return await message.answer(
            text="<b><i>HTML tags ('<' or '>') are not allowed in the text!</i></b>",
            reply_markup=await RKB.can()
        )

    await state.update_data(name=message.text)
    await state.set_state(FSMAdmin.addcar4)

    text = "<i>Please send the year of manufacture (e.g., 2023):</i>"
    await message.answer(text=text, reply_markup=await RKB.can())
    return None


"""------------------------------YEAR > SERVICES------------------------------"""


@router.message(FSMAdmin.addcar4, IsAdmin())
async def addcar4(message: Message, state: FSMContext):
    if message.text is None:
        return await message.answer(
            text="<b><i>No text detected! Please send the car's year of manufacture.</i></b>",
            reply_markup=await RKB.can()
        )

    if not message.text.isdigit() or str(message.text)[0] == "-":
        return await message.answer(
            text="<b><i>Please send a valid numeric year of manufacture !</i></b>",
            reply_markup=await RKB.can()
        )

    await state.update_data(addcar4=message.text)
    await state.set_state(FSMAdmin.addcar5)

    text = "<i>Please write a short description that will appear in the catalog:</i>"
    await message.answer(text=text, reply_markup=await RKB.can())
    return None


"""------------------------------SERVICES > CAPTION------------------------------"""


@router.message(FSMAdmin.addcar5, IsAdmin())
async def addcar5(message: Message, state: FSMContext):
    if message.text is None:
        return await message.answer(
            text="<b><i>No text detected! Please write a short description of the car's rental services.</i></b>",
            reply_markup=await RKB.can()
        )

    if "<" in message.text or ">" in message.text:
        return await message.answer(
            text="<b><i>HTML tags ('<' or '>') are not allowed!</i></b>",
            reply_markup=await RKB.can()
        )

    await state.update_data(addcar5=message.html_text)
    await state.set_state(FSMAdmin.addcar6)

    text = "<i>Please write a detailed description for the car profile:</i>"
    await message.answer(text=text, reply_markup=await RKB.can())
    return None


"""------------------------------CAPTION > PHOTOS------------------------------"""


@router.message(FSMAdmin.addcar6, IsAdmin())
async def addcar6(message: Message, state: FSMContext):
    if message.text is None:
        return await message.answer(
            text="<b><i>No text detected! Please write a full description for the car profile.</i></b>",
            reply_markup=await RKB.can()
        )

    if "<" in message.text or ">" in message.text:
        return await message.answer(
            text="<b><i>HTML tags ('<' or '>') are not allowed!</i></b>",
            reply_markup=await RKB.can()
        )

    await state.update_data(addcar6=message.html_text)
    await state.update_data(media=[])
    await state.set_state(FSMAdmin.addcar7)

    text = "<i>Please send photo media groups or individual photos.\n\nOnce you're done uploading photos, press the button below - <b>\"Continue\"</b>:</i>"
    photo = FSInputFile(SAMPLE_MEDIA_GROUP_PATH)
    await bot.send_photo(
        chat_id=message.chat.id,
        caption=text,
        photo=photo,
        reply_markup=await RKB.can_next()
    )
    return None


"""------------------------------PHOTOS > MAIN PHOTO------------------------------"""


@router.message(FSMAdmin.addcar7, IsAdmin())
async def addcar7(message: Message, state: FSMContext):
    if message.text == "➡️ Continue":
        data = await state.get_data()
        media = data['media']

        if not media:
            return await message.answer(
                text="<b><i>You have not uploaded any photos yet!</i></b>",
                reply_markup=await RKB.can_next()
            )

        await state.set_state(FSMAdmin.addcar8)

        text = "<i>Please send the main photo that will be displayed in the catalog:</i>"
        return await message.answer(text=text, reply_markup=await RKB.can())

    if not message.photo and not message.video:
        return await message.answer(
            text="<b><i>No media detected!</i></b>",
            reply_markup=await RKB.can_next()
        )

    if not message.photo:
        return await message.answer(
            text="<b><i>This is not a photo!</i></b>",
            reply_markup=await RKB.can_next()
        )

    data = await state.get_data()
    media = data['media']
    media.append(f"photo:{message.photo[0].file_id}")

    await state.update_data(media=media)
    return None


"""------------------------------MAIN PHOTO > VIDEOS------------------------------"""


@router.message(FSMAdmin.addcar8, IsAdmin())
async def addcar8(message: Message, state: FSMContext):
    if not message.photo:
        return await message.answer(
            text="<b><i>No media detected!</i></b>",
            reply_markup=await RKB.can()
        )

    if await state.get_state() != FSMAdmin.addcar9:
        text = "<i>Please send video media groups or individual videos:</i>"
        await message.answer(text=text, reply_markup=await RKB.can_next())

        data = await state.get_data()
        media = data['media']
        media.append(f"main_photo:{message.photo[0].file_id}")

        await state.update_data(media=media)
        await state.set_state(FSMAdmin.addcar9)
    return None


"""------------------------------VIDEOS > TAGS------------------------------"""


@router.message(FSMAdmin.addcar9, IsAdmin())
async def addcar9(message: Message, state: FSMContext):
    if message.photo:
        return await message.answer(
            text="<b><i>This is not a video!</i></b>",
            reply_markup=await RKB.can_next()
        )

    if not message.video and message.text not in ["➡️ Continue", "✅ Confirm"]:
        return await message.answer(
            text="<b><i>No media detected!</i></b>",
            reply_markup=await RKB.can_next()
        )

    data = await state.get_data()

    if message.text in ["➡️ Continue", "✅ Confirm"]:
        if message.text == "➡️ Continue":
            for media in data['media']:
                if media.split(":")[0] == "video":
                    break
            else:
                return await message.answer(
                    text="<b><i>Are you sure you want to skip adding videos and proceed without them?</i></b>",
                    reply_markup=await RKB.con_can()
                )

        tags = await get_tags()

        await state.set_state(FSMAdmin.addcar10)
        await state.update_data(addcar10=[])

        text = "<i>Select tags from the list below.\n\nSelected tags:</i>\n"
        return await message.answer(
            text=text,
            reply_markup=await IKB.tags(tags, data['car_id'])
        )

    media = data['media']
    media.append(f"video:{message.video.file_id}")
    await state.update_data(media=media)
    return None


"""------------------------------TAGS > CONTACTS------------------------------"""


@router.callback_query(FSMAdmin.addcar10, lambda query: query.data.split(":")[0] == "addtag", IsAdmin())
async def addcar10(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data["car_id"]

    if query.data.split(":")[-1] != user_id:
        return None

    if query.data.split(":")[1] == "add":
        tags = data['addcar10']

        if not tags:
            return await query.message.answer(text="<b><i>You haven't selected any tags!</i></b>")

        await state.set_state(FSMAdmin.addcar11)
        await query.message.edit_reply_markup(reply_markup=None)

        text = "<i>Please enter the contact information:</i>"
        await query.message.answer(text=text, reply_markup=await RKB.can())
        return None

    tag = ":".join(query.data.split(":")[1:-1])

    text_tags = list(
        map(
            lambda tag_: tag_.split("-  ", 1)[1] if "-  " in tag_ else None,
            query.message.text.split("\n")[1:]
        )
    )

    text_tags = [tag for tag in text_tags if tag is not None]

    tags = data['addcar10']
    tags_db = await get_tags()

    if tag not in tags:
        text = query.message.html_text
        await query.message.edit_text(text=f"{text}\n-  <code>{tag}</code>",
                                      reply_markup=await IKB.tags(tags_db, data['car_id']))
        tags.append(tag)
    else:
        index = int(text_tags.index(tag)) + 1
        text = query.message.html_text.split("\n")
        text.pop(index)
        text = "\n".join(text)

        await query.message.edit_text(text=text,
                                      reply_markup=await IKB.tags(tags_db, data['car_id']))
        tags.remove(tag)

    await state.update_data(set_tags=tags)
    return None


"""------------------------------CONTACTS > DAYS------------------------------"""


@router.message(FSMAdmin.addcar11, IsAdmin())
async def addcar11(message: Message, state: FSMContext):
    if message.text is None:
        return await message.answer(
            text="<b><i>No text detected! Please enter contact information.</i></b>",
            reply_markup=await RKB.can()
        )

    if "<" in message.text or ">" in message.text:
        return await message.answer(
            text="<b><i>HTML tags ('<' or '>') are not allowed!</i></b>",
            reply_markup=await RKB.can()
        )

    await state.update_data(addcar11=message.html_text)

    text = "<i>How many days should this car remain active in the catalog?\n\n" \
           "(<b>If skipped, it will be active for 30 days by default.</b>)</i>"
    await message.answer(text=text, reply_markup=await RKB.can_skip())

    await state.set_state(FSMAdmin.addcar12)
    return None


"""------------------------------DAYS > CALLBACKS------------------------------"""


@router.message(FSMAdmin.addcar12, IsAdmin())
async def addcar12(message: Message, state: FSMContext):
    if message.text is None:
        return await message.answer(
            text="<b><i>No text detected! Please enter the number of active days or skip.</i></b>",
            reply_markup=await RKB.can_skip()
        )

    if not message.text.isdigit() and message.text != "⏭ Skip":
        return await message.answer(
            text="<b><i>Please send a valid numeric value!</i></b>",
            reply_markup=await RKB.can_skip()
        )

    await state.update_data(addcar12=message.text if message.text.isdigit() else 30)

    data = await state.get_data()
    medias = data['media']
    main_photo = ""

    for media in medias:
        if media.split(":")[0] == "main_photo":
            main_photo = media.split(":", 1)[1]

    services = data['addcar5']
    tags = ",  ".join([f"<code>{tag}</code>" for tag in data['addcar10']])

    await bot.send_photo(
        chat_id=message.chat.id,
        photo=main_photo,
        caption=f"{services}\n\n{tags}",
        reply_markup=await IKB.car_info(data['car_id'])
    )

    text = "<i>Please review the information and confirm or cancel the addition.\n\n" \
           "(<b>Cancel | Confirm</b>)</i>"

    await message.answer(text=text, reply_markup=await RKB.con_can())
    await state.set_state(FSMAdmin.addcar13)
    return None


"""------------------------------CALLBACKS > CONFIRM------------------------------"""


@router.callback_query(FSMAdmin.addcar13, lambda query: query.data.split(":")[0] == "addcar", IsAdmin())
async def addcar13(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data["car_id"]

    if query.data.split(":")[-1] != user_id:
        return

    if query.data.split(":")[1] == "info":
        country = data['country']
        city = data['city']
        name = data['name']
        year = data['addcar4']
        caption = data['addcar6']
        medias = data['media']
        tags = ",  ".join([f"<code>{tag}</code>" for tag in data['addcar10']])

        media_group = await create_media_group(medias)
        text = TEXT_CAPTION_CAR.replace("<b>", "*").replace("</b>", "*").format(name, country, city, year, tags,
                                                                                caption)

        message_ids_list = []

        if len(media_group) > 10:
            one_group = []
            for media in media_group:
                one_group.append(media)
                if len(one_group) == 10:
                    var1 = await bot.send_media_group(chat_id=query.message.chat.id, media=one_group)
                    message_ids_list += [msg.message_id for msg in var1]
                    one_group = []
            if one_group:
                var1 = await bot.send_media_group(chat_id=query.message.chat.id, media=one_group)
                message_ids_list += [msg.message_id for msg in var1]
        else:
            var1 = await bot.send_media_group(chat_id=query.message.chat.id, media=media_group)
            message_ids_list += [msg.message_id for msg in var1]

        var2 = await query.message.answer(text=text, reply_markup=await IKB.car_back_contacts(data['car_id']))
        await query.message.delete()

        message_ids_list.append(var2.message_id)
        await state.update_data(msgs=message_ids_list)

    elif query.data.split(":")[1] == "backinfo":
        medias = data['media']
        main_photo = [media.split(":", 1)[1] for media in medias if media.split(":", 1)[0] == "main_photo"][0]
        message_ids = data['msgs']

        for message_id in message_ids:
            try:
                await bot.delete_message(chat_id=query.message.chat.id, message_id=message_id)
            except Exception:
                pass

        await bot.send_photo(chat_id=query.message.chat.id, photo=main_photo,
                             reply_markup=await IKB.car_info(data['car_id']))

    elif query.data.split(":")[1] == "contacts":
        message_ids = data['msgs']

        for message_id in message_ids:
            try:
                await bot.delete_message(chat_id=query.message.chat.id, message_id=message_id)
            except Exception:
                pass

        contacts = data['addcar11']

        await bot.send_message(chat_id=query.message.chat.id, text=contacts,
                               reply_markup=await IKB.car_back_to_info(data['car_id']), disable_web_page_preview=True)


"""------------------------------CONFIRM------------------------------"""


@router.message(FSMAdmin.addcar13, F.text == "✅ Confirm", IsAdmin())
async def addcar14(message: Message, state: FSMContext):
    data = await state.get_data()

    user_id = data['car_id']
    country = data['country']
    city = data['city']
    name = data['name']
    year = data['addcar4']
    services = data['addcar5']
    caption = data['addcar6']
    medias = data['media']
    tags = data['addcar10']
    contacts = data['addcar11']
    days = data['addcar12']

    await add_car_to_db(user_id, country, city, name, year, services, caption, medias, tags, contacts, days)
    await start_car_db_scheduler(user_id, int(days))

    text = f"<i>A new car has been added by user - <b>\"{message.from_user.full_name}\"</b></i>;\n\n" \
           f"Car model name: <b><code>{name}</code></b>;\n" \
           f"Car Telegram ID: <b><code>{user_id}</code></b>"

    await bot.send_message(chat_id=ADMIN_ID, text=text)

    logger.debug(f"NEW CAR ADDED: car_name - {name} ; car_id - {user_id}")

    await state.clear()
