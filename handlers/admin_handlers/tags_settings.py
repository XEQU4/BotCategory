from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from FSM import FSMAdmin
from config import ADMIN_ID
from database.main import get_tags, add_tag, del_tag
from dispatcher import bot
from filters import IsAdmin
from handlers.admin_handlers.keyboards import RKB, IKB
from logger.create_logger import logger

router = Router()

"""------------------------------| Command - set_tags | Text - 🏷 Manage tags" |------------------------------"""


@router.message(F.text == "🏷 Manage tags", IsAdmin())
@router.message(Command("set_tags"), IsAdmin())
async def command_set_tags_handling(message: Message, state: FSMContext):
    await state.clear()

    tags = await get_tags()
    text = "Here are all the existing tags in your bot:"

    if not tags:
        text = "Currently, there are no saved tags in the database, but you can add them yourself by clicking " \
               "the button below <b>\"➕ Add new\"</b> 👇"

    await message.answer(text=text,
                         reply_markup=await IKB.tags(tags))


@router.callback_query(F.data == "tag:back", IsAdmin())
async def cb_tag_back(query: CallbackQuery, state: FSMContext):
    await state.clear()

    tags = await get_tags()
    text = "Here are all the existing tags in your bot:"

    if not tags:
        text = "Currently, there are no saved tags in the database, but you can add them yourself by clicking " \
               "the button below <b>\"➕ Add new\"</b> 👇"

    await query.message.edit_text(text=text,
                                  reply_markup=await IKB.tags(tags))


"""------------------------------| Callback data - tag:add |------------------------------"""


@router.callback_query(F.data == "tag:add", IsAdmin())
async def cb_add_tag(query: CallbackQuery, state: FSMContext):
    text = "Enter the name of the tag:"

    await query.message.answer(text=text)

    await state.set_state(FSMAdmin.addtag1)


@router.message(FSMAdmin.addtag1, IsAdmin())
async def addtag1(message: Message, state: FSMContext):
    if message.text is None:
        text = "<i><b>Tag name cannot be empty!</b></i>"
        return await message.answer(text=text,
                                    reply_markup=await RKB.can())

    if "#" in message.text:
        text = "<i><b>Sorry, due to database structure the character \"#\" cannot be used when adding tags!</b></i>"
        return await message.answer(text=text,
                                    reply_markup=await RKB.can())

    if message.text in ["add", "back"] or \
            ":" in message.text and ("del" in message.text.split(":") or "del_conf" in message.text.split(":")):
        text = "<i><b>Sorry, the words \"add\", \"del\", \"back\", \"del_conf\" cannot be used as tag names!</b></i>"
        return await message.answer(text=text,
                                    reply_markup=await RKB.can())

    tags = await get_tags()

    if message.text in tags:
        text = "<i><b>Such tag already exists!</b></i>"
        return await message.answer(text=text)

    text = "Confirm the tag addition\n(<b>Cancel | Confirm</b>):"

    await message.answer(text=text,
                         reply_markup=await RKB.con_can())

    await state.update_data(tag=message.text)
    await state.set_state(FSMAdmin.addtag2)
    return None


@router.message(FSMAdmin.addtag2, F.text == "✅ Confirm", IsAdmin())
async def addtag2(message: Message, state: FSMContext):
    data = await state.get_data()
    tag = data['tag']

    await add_tag(tag)
    await state.clear()

    text = f"<i>New tag added by user - <b>\"{message.from_user.full_name}\"</b></i>;\n\nTag: \"<b><code>{tag}</code></b>\""

    # for admin_id in ADMIN_IDS:
    await bot.send_message(chat_id=ADMIN_ID,
                           text=text,
                           reply_markup=await RKB.admin_start())

    text = "Here are all the existing tags in your bot:"
    tags = await get_tags()
    await message.answer(text=text,
                         reply_markup=await IKB.tags(tags))

    logger.debug(f"ADMIN ADDED A NEW TAG - user_id: {message.from_user.id} ; tag: {tag}")


"""------------------------------| Callback data - tag:del |------------------------------"""


@router.callback_query(lambda query: query.data.split(":")[0] == "tag" and query.data.split(":")[1] not in ["add", "del", "back", "del_conf"], IsAdmin())
async def del_tag1(query: CallbackQuery):
    tag_name = query.data.split(":", 1)[1]

    await query.message.edit_reply_markup(reply_markup=await IKB.del_tag(tag_name))


@router.callback_query(lambda query: query.data.split(":")[0] == "tag" and query.data.split(":")[1] == "del", IsAdmin())
async def del_tag2(query: CallbackQuery):
    tag_name = query.data.split(":", 2)[2]

    await query.message.edit_reply_markup(reply_markup=await IKB.del_tag_confirm(tag_name))


@router.callback_query(lambda query: query.data.split(":")[0] == "tag" and query.data.split(":")[1] == "del_conf", IsAdmin())
async def del_tag3(query: CallbackQuery):
    tag = query.data.split(":", 2)[2]

    await del_tag(tag)

    text = f"<i>Tag deleted by user - <b>\"{query.from_user.full_name}\"</b></i>;\n\nTag: \"<b><code>{tag}</code></b>\""

    # for admin_id in ADMIN_IDS:
    await bot.send_message(chat_id=ADMIN_ID,
                           text=text,
                           reply_markup=await RKB.admin_start())

    tags = await get_tags()

    text = "Here are all the existing tags in your bot:"

    if not tags:
        text = "Currently, there are no saved tags in the database, but you can add them yourself by clicking " \
               "the button below <b>\"Add\"</b> 👇"

    await query.message.edit_text(text=text,
                                  reply_markup=await IKB.tags(tags))

    logger.debug(f"ADMIN DELETED A TAG - user_id: {query.from_user.id} ; tag: {tag}")
