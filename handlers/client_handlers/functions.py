from typing import Union

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message


async def add_msg_ids(message_ids: list[Union[int, str]], state: FSMContext) -> None:
    """
    Add message_id to state data

    :param state: FSMContext object
    :param message_ids: Message ids list
    """
    try:
        data = await state.get_data()
        msgs = list(data['msgs'])

    except Exception:
        msgs = [int(message_id) for message_id in message_ids]

    else:
        for message_id in message_ids:
            msgs.append(message_id)

    await state.update_data(msgs=msgs)


async def client_in_bot(state: FSMContext) -> bool:
    """
    Check the client in the bot

    :param state: FSMContext object
    :return: bool
    """
    try:
        data = await state.get_data()
        assert data['msgs']

    except Exception:
        return False

    else:
        return True


async def set_old_index_and_new_index_tags(query: CallbackQuery, count: Union[int, str], old_index: Union[int, str]) -> [[int, int], None]:
    """
    Create first and last index to send list cars

    :param query: CallbackQuery object
    :param count: Count of cars
    :param old_index: First tag index
    :return: [First car index, Last car index]
    """
    count = int(count)
    old_index = int(old_index)

    if isinstance(query, CallbackQuery) and query.data == "tag_back":
        if count <= 9 or old_index <= 9:
            return None

        if count % 9 == 0 and count == old_index:
            new_index = old_index - 9

        elif count == old_index:
            new_index = old_index - (old_index % 9)

        else:
            new_index = old_index - 9

        old_index = new_index - 9

    elif isinstance(query, CallbackQuery) and query.data == "tag_forw":
        if count <= 9 or old_index == count:
            return None

        if count - (count % 9) == old_index:
            new_index = count

        else:
            new_index = old_index + 9

    else:
        if count == 0:
            return None

        elif count % 9 == count:
            new_index = count

        else:
            new_index = old_index + 9

    return [old_index, new_index]


async def create_tags_text(tags: list[str]) -> str:
    """
    Create tags text for text sender tags

    :param tags: list - ['tag1', 'tag2' . . ., 'tagn']
    :return: tags mini text
    """

    if tags:
        tags_text = "\n" + "\n".join([f"`<code>{tag}</code>`" for tag in tags])

        return tags_text

    return ""


async def set_f_and_l_car_indexes(message: Union[Message, CallbackQuery], count: Union[int, str], f_index: Union[int, str]) -> [int, int]:
    """
    Create first and last index to send list cars

    :param message: aiogram.types.Message object
    :param count: Count of cars
    :param f_index: First car index
    :return: [First car index, Last car index]
    """
    count = int(count)
    len_ = int(f_index)

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

        if count % 5 == count:
            new_len_ = count

        else:
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

    else:
        if len_ == 0:
            if count % 5 == count:
                new_len_ = count

            else:
                new_len_ = 5

        elif count % 5 == count:
            new_len_ = count
            len_ = 0

        else:
            if len_ % 5 != 0:
                new_len_ = len_
                len_ = len_ - (len_ % 5)

            else:
                new_len_ = len_
                len_ -= 5

    return [len_, new_len_]


async def check_count_car(query_message: Union[Message, CallbackQuery], count: Union[int, str], data: dict) -> bool:
    """
    Checking whether a given button can be processed

    :param query_message: Message or CallbackQuery object
    :param count: Number of cars
    :param data: FSMContext object data (dict)
    :return: bool - Returns the permission to handle the button
    """
    if isinstance(query_message, Message) and query_message.text == "⬅️":
        return False

    elif isinstance(query_message, Message) and query_message.text in ["◀️", "▶️", "⏪", "⏩"]:
        if query_message.text in ["◀️", "⏪"] and int(data["f_index"]) <= 5:
            return True

        elif query_message.text in ["▶️", "⏩"] and int(data["f_index"]) >= int(count):
            return True

        else:
            return False

    elif isinstance(query_message, Message):
        return True

    else:
        return False