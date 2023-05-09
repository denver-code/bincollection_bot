from aiogram import types, dispatcher

from core.models.user import Location as LocationModel, User as UserModel
from core.redis import is_user_exist, set_user, get_user
from core.schedule import is_actual

async def set_user_location_event(message: types.Message, state: dispatcher.FSMContext):
    await state.finish()
    if not message.text.isdigit():
        return await message.answer("Looks like your UPRN number are invalid. Try again!")
    
    _location = LocationModel(UPRN=message.text)
    
    if not is_user_exist(message.from_id):
        _user = UserModel(
            id=message.from_id,
            is_subscribed=False,
            location=_location
        )
        set_user(message.from_id, _user.to_json())
        return await message.answer("Welcome in our team! Now you able to use every function. Type /menu to check them out!")

    _user = get_user(message.from_id)
    _user["location"] = _location.to_json()

    set_user(message.from_id, _user)
    await message.answer("Location updated successfully!")


async def fetch_user_event(message: types.Message, state: dispatcher.FSMContext):
    is_actual(message.from_id, force=True)

    await message.answer("User updated successfully!")