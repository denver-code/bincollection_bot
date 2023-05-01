from aiogram import Bot, Dispatcher
from aiogram.utils import executor       
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from core.config import settings

from bot.handlers import setup as handlers_setup

bot = Bot(token=settings.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


if __name__ == '__main__':
    handlers_setup.setup(dp)
    executor.start_polling(dp)