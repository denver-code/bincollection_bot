from aiogram import Dispatcher

from bot.handlers.callback import user

def setup(dp: Dispatcher):
    user.setup(dp)
