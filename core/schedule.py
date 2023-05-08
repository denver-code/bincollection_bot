from core.redis import get_user, set_user
from core.scraper import Scraper, expand_for_json
from datetime import datetime, timedelta


def clean_schedule(schedule: list) -> list:
    for day in schedule:
       if check_date_status(day["collection_day"]) == "past":
           schedule.remove(day)
    
    return schedule


def check_date_status(collection_date: str):
    try:
        collection_date = datetime.strptime(collection_date, "%Y-%m-%d").date()
    except ValueError:
        return "past"

    today = datetime.today().date()
    tomorrow = today + timedelta(days=1)

    if collection_date == today:
        return "today"
    elif collection_date == tomorrow:
        return "tomorrow"
    elif collection_date > today:
        return "feature"
    else:
        return "past"
    

def sort_schedule(schedule: list) -> list:
    schedule = clean_schedule(schedule)
    return sorted(schedule, key=lambda x: datetime.strptime(x["collection_day"], "%Y-%m-%d").date())


def add_extra(days: list) -> list:
    for day in days:
        day["status"] = check_date_status(day["collection_day"])
        if day["status"] not in ["today", "tomorrow"]:
            day["days_left"] = (datetime.strptime(day["collection_day"], '%Y-%m-%d').date() - datetime.today().date()).days
        day["readble"] = datetime.strptime(day["collection_day"], '%Y-%m-%d').date().strftime('%d of %B, %A')
    return days


def collection_days(schedule: list) -> list:
    days = sort_schedule(schedule)
    days = add_extra(days)
    return days


def next_collection_days(schedule: list) -> list:
    days = sort_schedule(schedule)[:2]
    days = add_extra(days)
    return days


def is_actual(user_id: str) -> bool:
    _user = get_user(user_id)

    clean_schedule(_user["schedule"])

    if not _user["schedule"]:
        fetch_schedule(user_id, _user["location"]["uprn"])

    return True


def fetch_schedule(user_id: int, uprn: str) -> dict:
    parser = Scraper()

    schedule = expand_for_json(parser.scrape(f"/bin-day/?brlu-selected-address={uprn}"))

    schedule = clean_schedule(schedule)

    _user = get_user(user_id)

    _user["schedule"] = schedule

    set_user(user_id, _user)

    return schedule
