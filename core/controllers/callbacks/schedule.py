import aiohttp
from io import BytesIO
from aiogram.types import CallbackQuery, ChatActions, InputFile
from core.scraper import Scraper
from core.redis import get_user

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
    