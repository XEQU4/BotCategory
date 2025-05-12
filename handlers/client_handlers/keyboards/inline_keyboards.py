from typing import Union

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import COUNTRIES_AND_CITIES


class IKB:
    """
    Class with inline keyboard functions
    """

    @staticmethod
    async def cmd_start() -> InlineKeyboardMarkup:
        """
        1st row: (text='Yes! I need a car', cb='start')
        """
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Yes! I need a car!", callback_data="start")
            ]
        ])

    @staticmethod
    async def countries() -> InlineKeyboardMarkup:
        """
        n rows: (text=country, cb=country)
        """
        keyboard = [
            [InlineKeyboardButton(text=country, callback_data=country)] for country in COUNTRIES_AND_CITIES.keys()
        ]

        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @staticmethod
    async def cities(country: str) -> InlineKeyboardMarkup:
        """
        n rows: (text=city, cb=city)
        """
        keyboard = [
            [InlineKeyboardButton(text=city, callback_data=city)] for city in COUNTRIES_AND_CITIES[country]
        ]

        keyboard.append([InlineKeyboardButton(text="🌆 Back to change country", callback_data="start")])

        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @staticmethod
    async def select_tags_or_catalog() -> InlineKeyboardMarkup:
        """
        1st row: (text='Car catalog', cb='search')
        2nd row: (text='Tag selection', cb='tags')
        """
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Cars", callback_data="search")
            ]
        ])

    @staticmethod
    async def tags(tags: list, old_index: int, new_index: int) -> InlineKeyboardMarkup:
        """
        1st row: (text=tag, cb='tag:' + tag)
        2nd row: (text=tag, cb='tag:' + tag)
        3rd row: (text='«', cb='tag_back') - (text='»', cb='tag_forw') - (text='✅ Search', cb='search')
        """
        buttons_rows = []

        if tags:
            buttons_all = [InlineKeyboardButton(text=tag, callback_data=f"tag:{tag}") for tag in tags]

            buttons = buttons_all[old_index:new_index]

            row = []  # len - 3
            for button in buttons:
                row.append(button)

                if len(row) == 3:
                    buttons_rows.append(row)
                    row = []

            if row:
                buttons_rows.append(row)

        buttons_rows.append([
            InlineKeyboardButton(text="«", callback_data="tag_back"),
            InlineKeyboardButton(text="»", callback_data="tag_forw"),
            InlineKeyboardButton(text="✅ Search", callback_data="search"),
        ])
        buttons_rows.append([
            InlineKeyboardButton(text="◀️ Back", callback_data="search"),
            InlineKeyboardButton(text="🗑 Reset", callback_data="reset_tags")
        ])

        return InlineKeyboardMarkup(inline_keyboard=buttons_rows)

    @staticmethod
    async def catalog_info(car_id: Union[int, str]) -> InlineKeyboardMarkup:
        """
        1st row: (text='INFO', cb='car:' + car_id)
        """
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="👉 INFO", callback_data=f"car:{car_id}")
            ]
        ])

    @staticmethod
    async def car_info(car_id: Union[int, str]) -> InlineKeyboardMarkup:
        """
        1st row: (text='Contacts', cb='contacts:' + car_id) - (text='«', cb='search')
        """
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Contacts", callback_data=f"contacts:{car_id}")
            ],
            [
                InlineKeyboardButton(text="«", callback_data="search")
            ]
        ])

    @staticmethod
    async def car_contacts(car_id: Union[int, str]) -> InlineKeyboardMarkup:
        """
        1st row: (text='«', cb='car:' + car_id)
        """
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="«", callback_data=f"carс:{car_id}")
            ]
        ])
