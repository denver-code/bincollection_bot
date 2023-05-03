from core.redis import get_user, set_user

def is_actual(user_id: str) -> bool:
    _user = get_user(user_id)

    print(_user)