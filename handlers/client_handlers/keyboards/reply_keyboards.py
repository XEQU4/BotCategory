from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class RKB:
    """
    Class with reply keyboard functions
    """

    @staticmethod
    async def catalog(count: str) -> ReplyKeyboardMarkup:
        """
        1st row: ◀️ - or - ▶️ - or - ◀️ ▶️ - or - 🔴
        2nd row: '🗂 Sort' + '🏙 Change city'
        """
        index = int(count.split("/")[0])
        count = int(count.split("/")[1])

        keyboard = [[], [], []]

        if index > 5:
            keyboard[0].append(KeyboardButton(text="◀️"))

        if index != count:
            keyboard[0].append(KeyboardButton(text="▶️"))

        elif not keyboard[0]:
            keyboard[0].append(KeyboardButton(text="🔴"))

        keyboard[1].append(KeyboardButton(text="🗂 Sort"))
        keyboard[1].append(KeyboardButton(text="🏙 Change city"))
        keyboard[2].append(KeyboardButton(text="🌆 Change country"))

        return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=keyboard)

    @staticmethod
    async def car_info_back() -> ReplyKeyboardMarkup:
        """
        1st row: ⬅️
        """
        keyboard = [[]]

        keyboard[0].append(KeyboardButton(text="⬅️"))

        return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=keyboard)