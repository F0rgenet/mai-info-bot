from datetime import timedelta

from icalendar import Calendar, Event

from database.crud import crud_entry
from database.models import Entry


async def create_entry_event(entry: Entry):
    event = Event()
    event.add('name', f"{entry.subject.name} ({entry.type.name})")
    event.add('dtstart', entry.datetime)
    event.add('dtend', entry.datetime + timedelta(hours=1, minutes=30))
    return event


async def generate_ical_file(group: str):
    schedule_calendar = Calendar()
