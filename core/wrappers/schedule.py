from functools import wraps
from core.redis import is_user_exist
from core.states.location import LocationFetcher
from core.schedule import is_actual


def is_schedule_actual(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if is_actual(args[0].from_user.id):
            return await func(*args, **kwargs)
    return wrapper