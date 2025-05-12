import pytest
from aiogram import Bot


@pytest.mark.asyncio
async def test_bot_token_loading():
    from config import TOKEN

    assert TOKEN, "BOT_TOKEN should not be empty"
    bot = Bot(token=TOKEN)
    assert bot.token == TOKEN
