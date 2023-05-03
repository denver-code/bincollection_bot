import redis
import json

r = redis.Redis()


def get_user(id: str):
    dict_bytes = r.get(id)

    if not dict_bytes:
        return {}

    dict_str = dict_bytes.decode('utf-8')

    my_dict = json.loads(dict_str)

    return my_dict


def add_file(filename: str, content):
    # "calendars", {pdf_url.split("/")[-1]: pdf_content}
    print(content)
    r.set(filename, bytes(json.dumps({"content": content}), "utf-8"))

def set_user(id: str, data: dict):
    r.set(id, bytes(json.dumps(data), "utf-8"))


def logout(id: str):
    r.delete(id)


def is_subscribed(id: str) -> bool:
    return bool(get_user(id).get("is_subscribed"))


def toggle_subscription(id: str) -> bool:
    _user = get_user(id)
    _user["is_subscribed"] = not bool(_user["is_subscribed"])
    set_user(id, _user)

    return _user["is_subscribed"]


def is_user_exist(id: int) -> bool:
    return bool(get_user(id))
