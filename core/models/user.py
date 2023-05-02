from typing import Optional
from pydantic import BaseModel


class Location(BaseModel):
    UPRN: str

    def to_json(self):
        return {
            "uprn": self.UPRN
        }


class Schedule(BaseModel):
    schedule: list

    def to_list(self):
        return self.schedule


class User(BaseModel):
    id: int
    is_subscribed: bool
    location: Location
    schedule: Optional[Schedule]

    def to_json(self):
        _user = {
            "id": self.id,
            "is_subscribed": self.is_subscribed,
            "location": self.location.to_json(),
            "schedule": (self.schedule.to_list() if self.schedule != None else [])
        }
        return _user
