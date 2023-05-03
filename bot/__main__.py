from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from core.config import settings

from bot.handlers import setup as handlers_setup


bot = Bot(token=settings.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Start the bot"),
        types.BotCommand("menu", "Show all cool commands via menu!"),
    ])


def main():
    handlers_setup.setup(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=set_default_commands)


if __name__ == '__main__':
    main()
