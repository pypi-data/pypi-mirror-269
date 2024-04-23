from datetime import datetime, timedelta, date, time
from typing import Optional, List

from oldschool_management_tools.special_prompts.special_prompts import SPECIAL_PROMPTS
from oldschool_management_tools.calendar_items.calendar_item import CalendarItem
from oldschool_management_tools.calendar_integrator import CalendarIntegrator
from os import system, path
from dataclasses import dataclass
from re import match as re_match
import yaml

CATEGORIES_REQUIRING_PREP = ["green"]
system('color')


class CalendarReader:
    CONFIG_FILE = "management_tools_config.yaml"

    def __init__(self, integrator: CalendarIntegrator):
        self.cal_integrator = integrator
        if path.exists(CalendarReader.CONFIG_FILE):
            with open(CalendarReader.CONFIG_FILE, "r") as stream:
                config = yaml.safe_load(stream)
                self.config = config

    def _get_day_cal(self, cal_date: datetime) -> List[CalendarItem]:
        apt_items = self.cal_integrator.get_day_cal(cal_date)
        apt_items.sort(key=lambda x: x.start_datetime)
        return apt_items

    def fill_prep(self, parsed_day: datetime = datetime.today()):
        prep_duration = self.cal_integrator.PREP_DURATION
        apts = self.get_valid_apts(self._get_day_cal(parsed_day))
        free_slots: list[TimeSlot] = []
        last_apt_end_time: Optional[datetime] = None
        new_apts = []

        relevant_apts = [apt for apt in apts if apt.busy_status != 0]  # busy_status 0 == Free

        for apt in relevant_apts:
            if not free_slots:
                free_slots.append(TimeSlot(apt.start_datetime.replace(hour=8, minute=0, second=0), apt.start_datetime))
            elif last_apt_end_time and free_slots[-1].end_datetime < apt.start_datetime and last_apt_end_time < apt.start_datetime:
                # We have a free slot between the last appointment and this one, push it on the stack
                new_free_slot = TimeSlot(last_apt_end_time, apt.start_datetime)
                free_slots.append(new_free_slot)

            last_free_slot = free_slots[-1]
            if apt.category.lower() in CATEGORIES_REQUIRING_PREP and last_free_slot.end_datetime <= apt.start_datetime:
                prep_slot = TimeSlot(last_free_slot.end_datetime - timedelta(minutes=prep_duration),
                                     last_free_slot.end_datetime)
                last_free_slot.end_datetime = last_free_slot.end_datetime - timedelta(minutes=prep_duration)
                # If the free slot is now too small to use, pop it off the stack
                if last_free_slot.end_datetime - timedelta(minutes=prep_duration) < last_free_slot.start_datetime:
                    free_slots.pop()
                new_apts.append(CalendarItem(f"Prep {apt.name}", "Desk", "yellow",
                                             prep_slot.start_datetime, prep_slot.start_datetime.time(),
                                             prep_slot.end_datetime, prep_slot.end_datetime.time()))
            last_apt_end_time = apt.end_datetime

        [self.cal_integrator.add_apt(apt) for apt in new_apts]
        self.show_day_sched(parsed_day)

    def show_day_sched(self, parsed_day: datetime = datetime.today()):
        cal = self._get_day_cal(parsed_day)
        self.print_cal(cal)

    def wipe_prep(self, parsed_day: datetime = datetime.today()):
        cal = self._get_day_cal(parsed_day)
        cal_item_num = 0
        while len(cal) > cal_item_num + 1:
            cal_item = cal[cal_item_num]

            if cal_item.category == "yellow" and cal_item.name.startswith("Prep"):
                self.cal_integrator.delete_cal_item(parsed_day, cal_item)
                # Reload todays calendar, because outlook changes the index when we delete
                cal = self._get_day_cal(parsed_day)
            else:
                cal_item_num = cal_item_num + 1

    def get_valid_apts(self, cal: List[CalendarItem]) -> List[CalendarItem]:
        return [apt for apt in cal if not re_match(self.config['ignore_subject_regex'], str(apt.name))]

    def print_cal(self, cal: List[CalendarItem]):
        for apt in self.get_valid_apts(cal):
            if apt.busy_status != 0:
                apt.print()

    def prompt_day_tasks(self, parsed_day=datetime.today()):
        for spec_prompt in SPECIAL_PROMPTS:
            spec_prompt.show()
        apts = self.get_valid_apts(self._get_day_cal(parsed_day))
        for apt in apts:
            if apt.category.lower() in CATEGORIES_REQUIRING_PREP:
                input(f"Prep for {apt.name} => Done?")


def start_of_day(day: date) -> datetime:
    return datetime.combine(day, time())


def parse_day(day: str) -> datetime:
    match day:
        case None | '' | "today":
            return start_of_day(date.today())
        case "tomorrow":
            return start_of_day(date.today()) + timedelta(days=1)
        case d if day.isnumeric():
            return start_of_day(date.today()) + timedelta(days=int(d))
        case _:
            raise ValueError(f"Bad day [{day}]")


@dataclass
class TimeSlot:
    start_datetime: datetime
    end_datetime: datetime
