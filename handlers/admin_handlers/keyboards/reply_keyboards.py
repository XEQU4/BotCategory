from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import COUNTRIES_AND_CITIES


class RKB:
    """
    Class with reply keyboard functions for admin
    """

    @staticmethod
    async def admin_start() -> ReplyKeyboardMarkup:
        """
        Add car
        Manage cars | Manage tags
        Expiring list
        """
        return ReplyKeyboardMarkup(resize_keyboard=True,
                                   keyboard=[
                                       [
                                           KeyboardButton(text="➕ Add car"),
                                           KeyboardButton(text="⏳ Expiring list")
                                       ],
                                       [
                                           KeyboardButton(text="🛠 Manage cars"),
                                           KeyboardButton(text="🏷 Manage tags")
                                       ]
                                   ],
                                   one_time_keyboard=True)

    @staticmethod
    async def country_can() -> ReplyKeyboardMarkup:
        """
        Select country
        """
        keyboard = [
            [KeyboardButton(text=country)] for country in COUNTRIES_AND_CITIES.keys()
        ]

        keyboard.append([KeyboardButton(text="❌ Cancel")])

        return ReplyKeyboardMarkup(resize_keyboard=True,
                                   keyboard=keyboard,
                                   one_time_keyboard=True)

    @staticmethod
    async def city_can(country: str) -> ReplyKeyboardMarkup:
        """
        Select city
        """
        keyboard = [
            [KeyboardButton(text=city)] for city in COUNTRIES_AND_CITIES[country]
        ]

        keyboard.append([KeyboardButton(text="❌ Cancel")])

        return ReplyKeyboardMarkup(resize_keyboard=True,
                                   keyboard=keyboard,
                                   one_time_keyboard=True)

    @staticmethod
    async def country_can2() -> ReplyKeyboardMarkup:
        """
        Select multiple countries
        """
        keyboard = [
            [KeyboardButton(text=country)] for country in COUNTRIES_AND_CITIES.keys()
        ]

        keyboard.append([KeyboardButton(text="⏭ Skip")])
        keyboard[-1].append(KeyboardButton(text="✅ Done"))

        return ReplyKeyboardMarkup(resize_keyboard=True,
                                   keyboard=keyboard,
                                   one_time_keyboard=True)

    @staticmethod
    async def city_can2(country: str) -> ReplyKeyboardMarkup:
        """
        Select multiple cities
        """
        keyboard = [
            [KeyboardButton(text=city)] for city in COUNTRIES_AND_CITIES[country]
        ]

        keyboard.append([KeyboardButton(text="⏭ Skip")])
        keyboard[-1].append(KeyboardButton(text="✅ Done"))

        return ReplyKeyboardMarkup(resize_keyboard=True,
                                   keyboard=keyboard,
                                   one_time_keyboard=True)

    @staticmethod
    async def con_can() -> ReplyKeyboardMarkup:
        """
        Confirm or Cancel
        """
        return ReplyKeyboardMarkup(resize_keyboard=True,
                                   keyboard=[
                                       [
                                           KeyboardButton(text="❌ Cancel"),
                                           KeyboardButton(text="✅ Confirm")
                                       ]
                                   ],
                                   one_time_keyboard=True)

    @staticmethod
    async def con_can2() -> ReplyKeyboardMarkup:
        """
        Stop or Confirm
        """
        return ReplyKeyboardMarkup(resize_keyboard=True,
                                   keyboard=[
                                       [
                                           KeyboardButton(text="⛔ Stop"),
                                           KeyboardButton(text="✅ Confirm")
                                       ]
                                   ],
                                   one_time_keyboard=True)

    @staticmethod
    async def skip_can() -> ReplyKeyboardMarkup:
        """
        Skip or Confirm
        Done
        """
        return ReplyKeyboardMarkup(resize_keyboard=True,
                                   keyboard=[
                                       [
                                           KeyboardButton(text="⏭ Skip"),
                                           KeyboardButton(text="✅ Confirm")
                                       ],
                                       [
                                           KeyboardButton(text="✅ Done")
                                       ]
                                   ],
                                   one_time_keyboard=True)

    @staticmethod
    async def can_skip() -> ReplyKeyboardMarkup:
        """
        Cancel or Skip
        """
        return ReplyKeyboardMarkup(resize_keyboard=True,
                                   keyboard=[
                                       [
                                           KeyboardButton(text="❌ Cancel"),
                                           KeyboardButton(text="⏭ Skip")
                                       ]
                                   ],
                                   one_time_keyboard=True)

    @staticmethod
    async def can_next() -> ReplyKeyboardMarkup:
        """
        Cancel or Continue
        """
        return ReplyKeyboardMarkup(resize_keyboard=True,
                                   keyboard=[
                                       [
                                           KeyboardButton(text="❌ Cancel"),
                                           KeyboardButton(text="➡️ Continue")
                                       ]
                                   ],
                                   one_time_keyboard=True)

    @staticmethod
    async def can_next2() -> ReplyKeyboardMarkup:
        """
        Skip or Continue
        Done
        """
        return ReplyKeyboardMarkup(resize_keyboard=True,
                                   keyboard=[
                                       [
                                           KeyboardButton(text="⏭ Skip"),
                                           KeyboardButton(text="➡️ Continue")
                                       ],
                                       [
                                           KeyboardButton(text="✅ Done")
                                       ]
                                   ],
                                   one_time_keyboard=True)

    @staticmethod
    async def can() -> ReplyKeyboardMarkup:
        """
        Only Cancel
        """
        return ReplyKeyboardMarkup(resize_keyboard=True,
                                   keyboard=[
                                       [
                                           KeyboardButton(text="❌ Cancel")
                                       ]
                                   ],
                                   one_time_keyboard=True)

    @staticmethod
    async def can_fin() -> ReplyKeyboardMarkup:
        """
        Cancel or Done
        """
        return ReplyKeyboardMarkup(resize_keyboard=True,
                                   keyboard=[
                                       [
                                           KeyboardButton(text="❌ Cancel")
                                       ],
                                       [
                                           KeyboardButton(text="✅ Done")
                                       ]
                                   ],
                                   one_time_keyboard=True)

    @staticmethod
    async def skip() -> ReplyKeyboardMarkup:
        """
        Skip
        Done
        """
        return ReplyKeyboardMarkup(resize_keyboard=True,
                                   keyboard=[
                                       [
                                           KeyboardButton(text="⏭ Skip")
                                       ],
                                       [
                                           KeyboardButton(text="✅ Done")
                                       ]
                                   ],
                                   one_time_keyboard=True)

    @staticmethod
    async def cars_actinact(count: str) -> ReplyKeyboardMarkup:
        """
        Pagination buttons
        """
        len_ = int(count.split("/")[0])
        total = int(count.split("/")[1])

        keyboard = [[]]

        if len_ > 5:
            keyboard[0].append(KeyboardButton(text="⏪"))
            keyboard[0].append(KeyboardButton(text="◀️"))

        if len_ != total:
            keyboard[0].append(KeyboardButton(text="▶️"))
            keyboard[0].append(KeyboardButton(text="⏩"))

        if not keyboard[0]:
            keyboard[0].append(KeyboardButton(text="🔴"))

        return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=keyboard)
