import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# scheduler = BackgroundScheduler()
from core.config import settings

from bot.handlers import setup as handlers_setup
from core.redis import get_subscribed_users, set_user, ping as r_ping
from core.schedule import clean_schedule, is_actual, next_collection_days


loop = asyncio.get_event_loop()
scheduler = AsyncIOScheduler()
bot = Bot(token=settings.TOKEN, loop=loop)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Start the bot"),
        types.BotCommand("menu", "Show all commands via menu"),
        types.BotCommand("fetch", "Fetch your actual schedule from council website"),
        types.BotCommand("ping", "Check if bot in online"),
        types.BotCommand("time", "Check server time"),
    ])

async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


async def scheduler_job():
    subscribed = get_subscribed_users()

    for user in subscribed:
        user = is_actual(user["id"])
        days = next_collection_days(user["schedule"], extra = True)
        for day in days:
            _day_index = user["schedule"].index(day)

            if day["status"] == "tomorrow" and day["is_notified"] == False:

                day["is_notified"] = True

                await bot.send_message(user["id"], f"Hello, There's a {day['bin_type']} collection tomorrow!")

            if "status" in day:
                    _to_delete = ["status", "readble"]
                    for key in _to_delete:
                        del day[key]

            user["schedule"][_day_index] = day

            set_user(user["id"], user)
    

@dp.message_handler(commands=['ping'])
async def ping(message: types.Message):
    await message.answer("Pong!")

@dp.message_handler(commands=['time'])
async def time(message: types.Message):
    await message.answer(f"Server time is: {str(datetime.datetime.now())}")

def main():
    handlers_setup.setup(dp)
    scheduler.add_job(scheduler_job, 'cron', hour=20, minute=00)
    scheduler.start()
    executor.start_polling(dp, loop=loop, skip_updates=True, on_startup=set_default_commands, on_shutdown=shutdown)

    
if __name__ == '__main__':
    main()