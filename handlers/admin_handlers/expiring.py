from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.car_funcs import get_expiring_cars_names_ids, get_car_name, get_car_contacts
from filters import IsAdmin
from handlers.admin_handlers.keyboards import IKB, RKB

router = Router()

"""------------------------------GET_EXPIRING_CARS------------------------------"""


@router.message(F.text == "⏳ Expiring list", IsAdmin())
@router.message(Command("exp_list"), IsAdmin())
async def command_exp_list_handling(message: Message, state: FSMContext):
    await state.clear()

    exp_cars = await get_expiring_cars_names_ids()

    text = "Here are all the cars whose subscription expires in 3 days or less:"

    if not exp_cars:
        text = "<i>Currently, all cars have more than 3 days left, or there are no cars in the database, or all cars' subscriptions have already expired.</i>"

        await message.answer(text=text,
                             reply_markup=await RKB.admin_start())

    else:
        await message.answer(text=text,
                             reply_markup=await IKB.expiring(exp_cars))


@router.callback_query(F.data == "exp:back", IsAdmin())
async def cb_exp_back(query: CallbackQuery, state: FSMContext):
    await state.clear()

    exp_cars = await get_expiring_cars_names_ids()

    text = "Here are all the cars whose subscription expires in 3 days or less:"

    if not exp_cars:
        text = "<i>Currently, all cars have more than 3 days left.</i>"

        await query.message.edit_text(text=text)

    else:
        await query.message.edit_text(text=text,
                                      reply_markup=await IKB.expiring(exp_cars))


"""------------------------------GET_CONTACTS------------------------------"""


@router.callback_query(lambda query: query.data.split(":")[0] == "exp", IsAdmin())
async def cb_exp(query: CallbackQuery):
    car_name = await get_car_name(query.data.split(":")[1])
    car_contacts = await get_car_contacts(query.data.split(":")[1])

    text = f"Car Name:\n" \
           f"<code>{car_name}</code>\n" \
           f"\n" \
           f"Contacts:\n" \
           f"{car_contacts}"

    await query.message.edit_text(text=text,
                                  reply_markup=await IKB.back_expiring())
