from aiogram import Dispatcher

from core.controllers.start import start_event


def setup(dp: Dispatcher):
    dp.register_message_handler(start_event, commands=["start"], state='*')
