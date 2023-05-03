from aiogram import Dispatcher
from core.controllers.menu import menu_event


def setup(dp: Dispatcher):
    dp.register_message_handler(menu_event, commands=["menu"], state='*')
