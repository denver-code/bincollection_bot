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
    created_timestamp: int

    def to_json(self):
        return {
            "schedule": self.schedule,
            "created_timestamp": self.created_timestamp
        }


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
            "schedule": (self.schedule.to_json() if self.schedule != None else {})
        }
        return _user
