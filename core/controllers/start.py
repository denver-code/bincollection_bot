from aiogram import types, dispatcher


async def start_event(message: types.Message, state: dispatcher.FSMContext):
    await message.answer("Welcome, mate!")