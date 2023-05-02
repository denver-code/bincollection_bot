from functools import wraps
from core.redis import is_user_exist
from core.states.location import LocationFetcher


def user_cache_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if is_user_exist(args[0].from_id):
            return await func(*args, **kwargs)

        await args[0].answer("We need your UPRN to fetch actual data from council website.\nPlease note that now our service works only with *Adur&Worthing Council*\n\nIf you don't know yuur UPRN you can check it here -https://www.findmyaddress.co.uk/search",
                             parse_mode="Markdown",)
        await LocationFetcher.UPRN.set()

    return wrapper
