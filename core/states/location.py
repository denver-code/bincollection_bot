from aiogram.dispatcher.filters.state import State, StatesGroup

class LocationFetcher(StatesGroup):
    UPRN = State()