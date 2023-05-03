from aiogram import Dispatcher

from bot.handlers.callbacks import user
from bot.handlers.callbacks import schedule

def setup(dp: Dispatcher):
    user.setup(dp)
    schedule.setup(dp)
