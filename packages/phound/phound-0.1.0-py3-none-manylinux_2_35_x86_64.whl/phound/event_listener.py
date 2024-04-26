from typing import TextIO

from phound import events
from phound.events import EventType, Event
from phound import exceptions


class EventListener:
    def __init__(self, source: TextIO) -> None:
        self._source = source

    def wait_event(self, *event_types: EventType, accept_any: bool = False) -> Event:
        event = self._get_next_event()
        if event.type == EventType.ERROR:
            raise exceptions.PhoundError(event.body)
        if event.type in event_types or (not event_types and accept_any):
            return event
        raise exceptions.UnexpectedEventError(
            f"Unexpected event: {event.type}, expected: {', '.join(event_types)}")

    def _get_next_event(self) -> Event:
        while True:
            data = self._source.readline()
            if not data:
                raise exceptions.InputError
            event = events.parse(data)
            if event:
                return event
