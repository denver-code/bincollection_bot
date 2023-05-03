from aiogram.types import CallbackQuery

from core.keyboards.menu import inline_menu_markup
from core.redis import toggle_subscription
from core.states.location import LocationFetcher


async def subscribe_toggle_callback_handler(callback_query: CallbackQuery):
    toggle_subscription(callback_query.from_user.id)
    await callback_query.message.edit_reply_markup(inline_menu_markup(callback_query.from_user.id))


async def adjust_location_callback_handler(callback_query: CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer("We need your UPRN to fetch actual data from council website.\nPlease note that now our service works only with *Adur&Worthing Council*\n\nIf you don't know yuur UPRN you can check it here -https://www.findmyaddress.co.uk/search",
                             parse_mode="Markdown",)
    await LocationFetcher.UPRN.set()
