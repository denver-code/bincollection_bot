from aiogram import Dispatcher

from core.controllers.callbacks.user import adjust_location_callback_handler, subscribe_toggle_callback_handler


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(subscribe_toggle_callback_handler, lambda c: c.data == "subscription_toggle")
    dp.register_callback_query_handler(adjust_location_callback_handler, lambda c: c.data == "adjust_location")
