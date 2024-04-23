from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import time, datetime
from termcolor import cprint


def nice_time_str(time_in_zone) -> str:
    return str(time_in_zone)[0:-3]


@dataclass_json
@dataclass
class CalendarItem:
    name: str
    location: str
    category: str
    start_datetime: datetime
    start_time: time
    end_datetime: datetime
    end_time: time
    busy_status: int = 2

    def print(self):
        cprint(f"{nice_time_str(self.start_time)} to {nice_time_str(self.end_time)} - {self.name} - {self.location}", self.category)

    @classmethod
    def from_outlook_apt(cls, apt):
        start_datetime = datetime.fromisoformat(str(apt.StartInStartTimeZone))
        start_time = time.fromisoformat(str(apt.StartInStartTimeZone.time()))
        end_datetime = datetime.fromisoformat(str(apt.EndInEndTimeZone))
        end_time = time.fromisoformat(str(apt.EndInEndTimeZone.time()))

        location = apt.Location
        category = apt.Categories.split(' ')[0].lower()
        busy_status = apt.BusyStatus
        match category:
            case '':
                category = 'blue'
            case 'orange':
                category = 'yellow'
            case 'purple':
                category = 'magenta'
        return CalendarItem(apt.Subject, location, category, start_datetime, start_time, end_datetime, end_time, busy_status)


