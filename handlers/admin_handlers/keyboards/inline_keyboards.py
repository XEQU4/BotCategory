from typing import Union, Any
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class IKB:
    """
    Class with inline keyboard functions for admin
    """

    @staticmethod
    async def tags(tags: list, car_id: Union[int, str] = None) -> InlineKeyboardMarkup:
        buttons_rows = []

        if tags:
            if car_id is None:
                buttons_all = [InlineKeyboardButton(text=tag, callback_data=f"tag:{tag}") for tag in tags]
            else:
                buttons_all = [InlineKeyboardButton(text=tag, callback_data=f"addtag:{tag}:{car_id}") for tag in tags]

            row = []
            for button in buttons_all:
                row.append(button)

                if len(row) == 2:
                    buttons_rows.append(row)
                    row = []

            if row:
                buttons_rows.append(row)

        if car_id is None:
            buttons_rows.append([InlineKeyboardButton(text="➕ Add new", callback_data="tag:add")])
        else:
            buttons_rows.append([InlineKeyboardButton(text="✅ Done!", callback_data=f"addtag:add:{car_id}")])

        return InlineKeyboardMarkup(inline_keyboard=buttons_rows)

    @staticmethod
    async def del_tag(tag_name: str) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="«", callback_data="tag:back"),
                InlineKeyboardButton(text=tag_name, callback_data=f"passive_cb"),
                InlineKeyboardButton(text="🗑 Delete", callback_data=f"tag:del:{tag_name}")
            ]
        ])

    @staticmethod
    async def del_tag_confirm(tag_name: str) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="«", callback_data="tag:back"),
                InlineKeyboardButton(text=tag_name, callback_data=f"passive_cb"),
                InlineKeyboardButton(text="✅ Confirm", callback_data=f"tag:del_conf:{tag_name}")
            ]
        ])

    @staticmethod
    async def expiring(cars: list[Union[list, Any]]) -> InlineKeyboardMarkup:
        buttons_rows = []

        if cars:
            buttons_all = [InlineKeyboardButton(text=car[0], callback_data=f"exp:{car[1]}") for car in cars]

            row = []
            for button in buttons_all:
                row.append(button)
                if len(row) == 2:
                    buttons_rows.append(row)
                    row = []

            if row:
                buttons_rows.append(row)

        return InlineKeyboardMarkup(inline_keyboard=buttons_rows)

    @staticmethod
    async def back_expiring() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="« Back", callback_data="exp:back"),
            ]
        ])

    @staticmethod
    async def car_info(car_id: Union[int, str]) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="👉 Info", callback_data=f"addcar:info:{car_id}")
            ]
        ])

    @staticmethod
    async def car_back_contacts(car_id: Union[int, str]) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="«", callback_data=f"addcar:backinfo:{car_id}"),
                InlineKeyboardButton(text="📞 Contacts", callback_data=f"addcar:contacts:{car_id}")
            ]
        ])

    @staticmethod
    async def car_back_to_info(car_id: Union[int, str]) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="«", callback_data=f"addcar:info:{car_id}"),
            ]
        ])

    @staticmethod
    async def cars_act_inact() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Inactive", callback_data=f"carset:inact"),
                InlineKeyboardButton(text="Active", callback_data=f"carset:act")
            ]
        ])

    @staticmethod
    async def car_info2(car_id: Union[int, str]) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="👉 Info", callback_data=f"carset:info:{car_id}")
            ]
        ])

    @staticmethod
    async def car_data_set(views: Union[str, int], days: Union[str, int]) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="«", callback_data=f"carset:bm"),
                InlineKeyboardButton(text=f"Views: {views}", callback_data=f"carset:views"),
                InlineKeyboardButton(text=f"Subscription days: {days}", callback_data=f"carset:days")
            ],
            [
                InlineKeyboardButton(text="🗑 Delete car", callback_data=f"carset:del_car")
            ],
            [
                InlineKeyboardButton(text="✏️ Edit car data", callback_data=f"carset:set")
            ]
        ])

    @staticmethod
    async def car_days_set(days: Union[str, int], flag="save") -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="- 1", callback_data=f"carset:days:-:{days}"),
                InlineKeyboardButton(text=f"{days}", callback_data=f"passive_cb"),
                InlineKeyboardButton(text="+ 1", callback_data=f"carset:days:+:{days}")
            ],
            [
                InlineKeyboardButton(text="÷ 2", callback_data=f"carset:days:/:{days}"),
                InlineKeyboardButton(text="× 2", callback_data=f"carset:days:*:{days}")
            ],
            [
                InlineKeyboardButton(text="«", callback_data=f"carset:inline_bd"),
                InlineKeyboardButton(text="💾 Save", callback_data=f"carset:days:{flag}:{days}")
            ]
        ])

    @staticmethod
    async def del_car() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="«", callback_data=f"carset:inline_bd"),
                InlineKeyboardButton(text="🗑 Confirm delete", callback_data=f"carset:del_conf")
            ]
        ])
