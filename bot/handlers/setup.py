from aiogram import Dispatcher

from bot.handlers import start
from bot.handlers import user
from bot.handlers import menu
from bot.handlers.callbacks import setup as callbacks

def setup(dp: Dispatcher):
    start.setup(dp)
    user.setup(dp)
    menu.setup(dp)
    callbacks.setup(dp)
