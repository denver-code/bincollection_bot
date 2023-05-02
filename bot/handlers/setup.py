from aiogram import Dispatcher

from bot.handlers import start
from bot.handlers import user


def setup(dp: Dispatcher):
    start.setup(dp)
    user.setup(dp)
