from aiogram import Dispatcher
from core.controllers.user import set_user_location_event, fetch_user_event
from core.states.location import LocationFetcher


def setup(dp: Dispatcher):
    dp.register_message_handler(set_user_location_event, content_types=['text'], state=LocationFetcher.UPRN)
    dp.register_message_handler(fetch_user_event, content_types=['text'], commands=['fetch'])
