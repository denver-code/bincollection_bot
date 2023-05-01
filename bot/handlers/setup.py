from aiogram import types, dispatcher, Dispatcher

from bot.handlers import start


def setup(dp: Dispatcher):
    start.setup(dp)