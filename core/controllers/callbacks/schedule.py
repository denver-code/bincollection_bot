import aiohttp
from io import BytesIO
from aiogram.types import CallbackQuery, ChatActions, InputFile
from core.schedule import next_collection_days, collection_days
from core.scraper import Scraper
from core.redis import get_user
from core.wrappers.schedule import is_schedule_actual

async def get_calendar_callback_handler(callback_query: CallbackQuery):
    await callback_query.message.bot.send_chat_action(callback_query.from_user.id, ChatActions.TYPING)
    await callback_query.message.edit_text("Please wait while we fetch your calendar....", reply_markup=None)
    
    _user = get_user(callback_query.from_user.id)

    scraper = Scraper()
    pdf = scraper.scrape_calendar_link(url = f"/bin-day/?brlu-selected-address={_user['location']['uprn']}")
    if not pdf:
        return await callback_query.message.edit_text("Looks like there're no any calendar data!\nIf you think that this is a mistake - you can report a bug using /report command!", parse_mode="Markdown")
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://www.adur-worthing.gov.uk{pdf}") as response:
            pdf_content = BytesIO(await response.read())

    pdf_file = InputFile(pdf_content, filename="calendar.pdf")
    await callback_query.message.answer_document(pdf_file)
    await callback_query.message.edit_text("Here's your calendar, enjoy!", reply_markup=None)
    

def add_extra(_message_text, days):
    for day in days:
        _day_text = f"*{day['bin_type']}* - *{day['readble']}*"
        if day["status"] == "today":
            _day_text += " (Today)"
        elif day["status"] == "tomorrow":
            _day_text += " (Tomorrow)"
        elif day["status"] == "feature":
            _day_text += f" (In {day['days_left']} days)"
        _day_text += "\n"
        _message_text += _day_text
    
    return _message_text

@is_schedule_actual
async def get_next_collection_callback_handler(callback_query: CallbackQuery):
    days = next_collection_days(get_user(callback_query.from_user.id)["schedule"])
    _message_text = "Here's your next collection days:\n\n"

    _message_text += add_extra(_message_text, days)

    _message_text += "\n\nIf you think that information are not right - send /fetch command to update your schedule!\nYou can also get your calendar using /calendar command!"
    await callback_query.message.edit_text(_message_text, reply_markup=None, parse_mode="Markdown")


@is_schedule_actual
async def get_schedule_collection_callback_handler(callback_query: CallbackQuery):
    days = collection_days(get_user(callback_query.from_user.id)["schedule"])
    _message_text = "Here's your collection days:\n\n"
    
    _message_text += add_extra(_message_text, days)

    _message_text += "\n\nIf you think that information are not right - send /fetch command to update your schedule!\nYou can also get your calendar using /calendar command!"
    await callback_query.message.edit_text(_message_text, reply_markup=None, parse_mode="Markdown")
    