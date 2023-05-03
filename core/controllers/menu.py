from aiogram import types, dispatcher
from core.keyboards.menu import inline_menu_markup
from core.redis import is_subscribed

from core.wrappers.user import user_cache_required


@user_cache_required
async def menu_event(message: types.Message, state: dispatcher.FSMContext):
    
    await message.answer(
        "How can I help you?",
        parse_mode="Markdown",
        reply_markup=inline_menu_markup(message.from_id)
    )
