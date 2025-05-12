from typing import Union

from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto, InputMediaVideo, Message, CallbackQuery

from database.car_funcs import set_car


async def create_media_group(medias: list[str], caption: str = None) -> list[Union[InputMediaPhoto, InputMediaVideo]]:
    """
    Create media group

    :param medias: list - ["photo:SHAIccnakskcsaHICSad", "photo:vcsdkvjhndkCKOSDc", "video:scsaidvnkvmMCKd", "main_photo:cvihdohvIHVDajdkvj", . . .]
    :param caption: str - Caption, text
    :return: list - media group
    """
    media_list = medias.copy()

    for md in media_list:
        if md.split(":", 1)[0] == "main_photo":
            media_list.remove(md)

    for md in media_list:
        if md.split(":", 1)[0] == "video":
            media_group = [InputMediaVideo(media=md.split(":", 1)[1], caption=caption)]
            media_list.remove(md)

            break

    else:
        media_group = [InputMediaPhoto(media=media_list.pop(0).split(":", 1)[1], caption=caption)]

    for md in media_list:
        if md.split(":", 1)[0] == "video":
            media_group.append(InputMediaVideo(media=md.split(":", 1)[1]))

        else:
            media_group.append(InputMediaPhoto(media=md.split(":", 1)[1]))

    return media_group


async def set_len_and_new_len(message: Union[Message, CallbackQuery], count: Union[int, str], len_: Union[int, str]) -> [int, int]:
    """
    Create first and last index to send list cars

    :param message: aiogram.types.Message object
    :param count: Count of cars
    :param len_: First car index
    :return: [First car index, Last car index]
    """
    count = int(count)
    len_ = int(len_)

    if isinstance(message, Message) and message.text == "◀️":
        if count % 5 == 0 and count == len_:
            new_len_ = len_ - 5

        elif count == len_:
            new_len_ = len_ - (len_ % 5)

        else:
            new_len_ = len_ - 5

        len_ = new_len_ - 5

    elif isinstance(message, Message) and message.text == "⏪":
        len_ = 0
        new_len_ = 5

    elif isinstance(message, Message) and message.text == "▶️":
        if count - (count % 5) == len_:
            new_len_ = count

        else:
            new_len_ = len_ + 5

    elif isinstance(message, Message) and message.text == "⏩":
        new_len_ = count

        if count % 5 == 0:
            len_ = new_len_ - 5

        else:
            len_ = count - (count % 5)

    elif isinstance(message, CallbackQuery) and message.data.split(":")[1] == "bm":
        if count % 5 == 0 and count == len_:
            new_len_ = len_
            len_ = new_len_ - 5

        elif count == len_:
            new_len_ = len_
            len_ = count - (len_ % 5)

        else:
            new_len_ = len_
            len_ = new_len_ - 5

    else:
        if count % 5 == count:
            new_len_ = count

        else:
            new_len_ = len_ + 5

    return [len_, new_len_]


async def check_count_car(query_message: Union[Message, CallbackQuery], count: Union[int, str], data: dict) -> bool:
    """
    Checking whether a given button can be processed

    :param query_message: Message or CallbackQuery object
    :param count: Number of cars
    :param data: FSMContext object data (dict)
    :return: bool - Returns the permission to handle the button
    """
    if isinstance(query_message, Message) and query_message.text in ["◀️", "▶️", "⏪", "⏩"]:
        if query_message.text in ["◀️", "⏪"] and int(data["len_"]) <= 5:
            return True

        elif query_message.text in ["▶️", "⏩"] and int(data["len_"]) >= int(count):
            return True

        else:
            return False

    elif isinstance(query_message, Message):
        return True

    else:
        return False


async def check_car_set_datas(state: FSMContext) -> bool:
    """
    Checking for changed car data

    :param state: FSMContext object
    :return: Returns permission to send a message indicating that car data has been changed and whether these changes can be saved
    """
    data = await state.get_data()

    flag = False

    car = data['car']
    car_id = car[0]

    try:
        country = data['set_country']
    except Exception:
        country = car[11]
    else:
        if not flag:
            if country != car[11]:
                flag = True

    try:
        city = data['set_city']
    except Exception:
        city = car[1]
    else:
        if not flag:
            if city != car[1]:
                flag = True

    try:
        name = data['set_name']
    except Exception:
        name = car[2]
    else:
        if not flag:
            if name != car[2]:
                flag = True

    try:
        year = data['set_year']
    except Exception:
        year = car[3]
    else:
        if not flag:
            if year != car[3]:
                flag = True

    try:
        services = data['set_services']
    except Exception:
        services = car[4]
    else:
        if not flag:
            if services != car[4]:
                flag = True

    try:
        caption = data['set_caption']
    except Exception:
        caption = car[5]
    else:
        if not flag:
            if caption != car[5]:
                flag = True

    try:
        medias = data['set_media']
    except Exception:
        medias = car[6]
    else:
        if not flag:
            if medias != car[6]:
                flag = True

    try:
        tags = data['set_tags']
    except Exception:
        tags = [tag.rstrip("</code>").lstrip("</code>") for tag in car[7].split(",  ")]
    else:
        if not flag:
            if tags != [tag.rstrip("</code>").lstrip("</code>") for tag in car[7].split(",  ")]:
                flag = True

    try:
        contacts = data['set_contacts']
    except Exception:
        contacts = car[8]
    else:
        if not flag:
            if contacts != car[8]:
                flag = True

    try:
        days = data['set_days']
    except Exception:
        days = car[9]
    else:
        if not flag:
            if days != car[9]:
                flag = True

    if flag:
        await set_car(car_id, country, city, name, year, services, caption, medias, tags, contacts, days)

    return flag
