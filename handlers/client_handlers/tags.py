from typing import Union

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.main import get_tags
from dispatcher import bot
from filters import IsClient
from handlers.client_handlers.functions import add_msg_ids, set_old_index_and_new_index_tags, create_tags_text
from handlers.client_handlers.keyboards import IKB
from handlers.client_handlers.texts.get_text import get_client_text

router = Router()


@router.callback_query(F.data == "tags", IsClient())
@router.message(F.text == "🗂 Sort", IsClient())
async def tags1(query_message: Union[CallbackQuery, Message], state: FSMContext):
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

    tags = await get_tags()
    count = len(tags)
    data = await state.get_data()

    car_tags = [] if not data.get('tags', False) else data['tags']
    old_index = 0 if not data.get('old_index', False) else data['old_index']

    tags_text = await create_tags_text(car_tags)
    text = (await get_client_text("tags.py", "tags1")).format(tags_text)

    indexes = await set_old_index_and_new_index_tags(query_message, count, old_index)
    await state.update_data(old_index=indexes[1])

    markup = await IKB.tags(tags, *indexes)

    if isinstance(query_message, CallbackQuery):
        var = await query_message.message.answer(text=text,
                                                 reply_markup=markup)

    else:
        var = await query_message.answer(text=text,
                                         reply_markup=markup)

    await state.update_data(markup=markup)
    await state.update_data(msgs=[])

    await add_msg_ids([var.message_id], state)


@router.callback_query(F.data.in_(['tag_back', 'tag_forw']), IsClient())
async def tags2(query: CallbackQuery, state: FSMContext):
    tags = await get_tags()
    data = await state.get_data()
    count = len(tags)

    old_index = data['old_index']

    indexes = await set_old_index_and_new_index_tags(query, count, old_index)

    await query.answer()

    if indexes is None:
        return

    await state.update_data(old_index=indexes[1])

    markup = await IKB.tags(tags, *indexes)

    var = await query.message.edit_reply_markup(reply_markup=await IKB.tags(tags, *indexes))

    await state.update_data(markup=markup)

    await add_msg_ids([var.message_id], state)


@router.callback_query(F.data.startswith("tag:"), IsClient())
async def tags3(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    car_tags = [] if not data.get('tags', False) else data['tags']
    tag = (query.data.split(":", 1))[1]

    await query.answer()

    if tag in car_tags:
        car_tags.remove(tag)

    else:
        car_tags.append(tag)

    tags_text = await create_tags_text(car_tags)
    text = (await get_client_text("tags.py", "tags1")).format(tags_text)

    await state.update_data(tags=car_tags)

    markup = data['markup']

    var = await query.message.edit_text(text=text,
                                        reply_markup=markup)

    await add_msg_ids([var.message_id], state)


@router.callback_query(F.data == "reset_tags", IsClient())
async def tags4(query: CallbackQuery, state: FSMContext):
    await state.update_data(tags=[])

    text = await get_client_text("tags.py", "tags2")
    await query.answer(text=text,
                       show_alert=True)

    tags_text = await create_tags_text([])
    text = (await get_client_text("tags.py", "tags1")).format(tags_text)

    await state.update_data(tags=[])

    data = await state.get_data()
    markup = data['markup']

    try:
        var = await query.message.edit_text(text=text,
                                            reply_markup=markup)

        await add_msg_ids([var.message_id], state)

    except Exception:
        pass
