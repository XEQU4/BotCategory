import asyncio

from aiogram import Router, exceptions
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent
from asyncpg import PostgresError

from config import ADMIN_ID
from dispatcher import bot
from logger.create_logger import logger

router = Router()


@router.error(ExceptionTypeFilter(exceptions.CallbackAnswerException))
async def error_handler_callback(event: ErrorEvent):
    logger.warning(
        f"\n\t[aiogram] CallbackAnswerException - Callback response exception\n\tevent error: {event.exception}\n\n\tCallback: {event.update.callback_query}\n\tUpdate: {event.update}\n")
    raise event.exception


@router.error(ExceptionTypeFilter(exceptions.TelegramNotFound))
async def error_handler_not_found(event: ErrorEvent):
    logger.warning(
        f"\n\t[aiogram] TelegramNotFound - Chat/User/Message not found\n\tevent error: {event.exception}\n\n\tMessage: {event.update.message}\n\tUpdate: {event.update}\n")
    raise event.exception


@router.error(ExceptionTypeFilter(exceptions.TelegramRetryAfter))
async def error_handler_retry_after(event: ErrorEvent):
    wait_seconds = event.exception.retry_after if hasattr(event.exception, 'retry_after') else int(
        str(event.exception).split()[-7])
    logger.warning(
        f"\n\t[aiogram] TelegramRetryAfter - Too many requests, sleeping for {wait_seconds} seconds...\n\tevent error: {event.exception}\n\n\tMessage: {event.update.message}\n\tUpdate: {event.update}\n")
    await asyncio.sleep(int(wait_seconds))


@router.error(ExceptionTypeFilter(exceptions.TelegramBadRequest))
async def error_handler_bad_request(event: ErrorEvent):
    logger.warning(
        f"\n\t[aiogram] TelegramBadRequest - Bad request sent\n\tevent error: {event.exception}\n\n\tMessage: {event.update.message}\n\tUpdate: {event.update}\n")
    raise event.exception


@router.error(ExceptionTypeFilter(exceptions.TelegramUnauthorizedError))
async def error_handler_unauthorized(event: ErrorEvent):
    logger.error(
        f"\n\t[aiogram] TelegramUnauthorizedError - Bot token is invalid or expired\n\tevent error: {event.exception}\n\n\tUpdate: {event.update}\n")
    await bot.send_message(ADMIN_ID, "❗ Bot token is invalid or expired. Immediate attention required!")


@router.error(ExceptionTypeFilter(exceptions.TelegramForbiddenError))
async def error_handler_forbidden(event: ErrorEvent):
    logger.warning(
        f"\n\t[aiogram] TelegramForbiddenError - Bot was removed from the chat\n\tevent error: {event.exception}\n\n\tUpdate: {event.update}\n")
    raise event.exception


@router.error(ExceptionTypeFilter(PostgresError))
async def error_handler_postgres(event: ErrorEvent):
    logger.warning(
        f"\n\t[asyncpg] PostgresError - Database operation error\n\tevent error: {event.exception}\n\n\tUpdate: {event.update}\n")
    await bot.send_message(ADMIN_ID, "❗ Database operation error detected!")
    raise event.exception


@router.error()
async def error_handler_default(event: ErrorEvent):
    logger.error(
        f"\n\t[aiogram] Unknown error occurred\n\tevent error: {event.exception}\n\n\tUpdate: {event.update}\n")
    await bot.send_message(ADMIN_ID, "❗ Unknown critical error occurred!")
    raise event.exception
