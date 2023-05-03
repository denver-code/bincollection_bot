from aiogram import types, dispatcher

from core.wrappers.user import user_cache_required


@user_cache_required
async def start_event(message: types.Message, state: dispatcher.FSMContext):
    await message.answer("Welcome, mate!\nYou can check our /menu to controll your subsctitption status.", parse_mode="Markdown", reply_markup=types.ReplyKeyboardRemove())
