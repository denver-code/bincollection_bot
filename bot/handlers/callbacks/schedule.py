from aiogram import Dispatcher

from core.controllers.callbacks.schedule import get_calendar_callback_handler


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(get_calendar_callback_handler, lambda c: c.data == "calendar_schedule")