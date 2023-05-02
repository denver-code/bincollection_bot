from aiogram import types, dispatcher

from core.wrappers.user import user_cache_required


@user_cache_required
async def start_event(message: types.Message, state: dispatcher.FSMContext):
    await message.answer("Welcome, mate!")
