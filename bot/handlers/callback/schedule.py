from aiogram import Dispatcher
from aiogram.types import CallbackQuery


async def subscribe_toggle_callback_handler(callback_query: CallbackQuery):
    await callback_query.message.answer("")
    await callback_query.message.delete()


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(subscribe_toggle_callback_handler, lambda c: c.data == "login_via_token")