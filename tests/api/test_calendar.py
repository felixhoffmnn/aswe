# pylint: disable=no-value-for-parameter
import pytest

from aswe.api.calendar import (
    Event,
    create_event,
    get_all_events_today,
    get_events_by_timeframe,
    get_next_event_today,
)


def test_event_required_fields() -> None:
    """Test required fields for `Event` dataclass"""
    with pytest.raises(TypeError):
        Event()  # type: ignore


def test_event_variable_types() -> None:
    """Test variable types for `Event` dataclass"""
    event = Event(
        title="Title",
        description="Description",
        location="location",
        full_day=False,
        date="",
        start_time="2022-12-23T08:00:00+01:00",
        end_time="2022-12-23T09:00:00+01:00",
    )

    assert isinstance(event.title, str)
    assert isinstance(event.description, str)
    assert isinstance(event.location, str)
    assert isinstance(event.full_day, bool)
    assert isinstance(event.date, str)
    assert isinstance(event.start_time, str)
    assert isinstance(event.end_time, str)


def test_get_events_by_timeframe() -> None:
    """Test `aswe.api.calendar.get_events_by_timeframe`"""
    events = get_events_by_timeframe("2022-10-19T00:00:00.000001Z", "2022-10-19T23:59:59.999999Z")

    assert isinstance(events, list)
    assert len(events) == 4
    assert isinstance(events[0], Event)
    assert isinstance(events[1], Event)
    assert isinstance(events[2], Event)
    assert isinstance(events[3], Event)


def test_get_all_events_today() -> None:
    """Test `aswe.api.calendar.get_all_events_today`"""
    events = get_all_events_today()

    assert isinstance(events, list)


def test_get_next_event_today() -> None:
    """Test `aswe.api.calendar.get_next_event_today`"""
    event = get_next_event_today()

    assert event is None or isinstance(event, Event)


@pytest.mark.skip(reason="Avoid mass creation of calendar entries")
def test_create_event() -> None:
    """Test `aswe.api.calendar.get_next_event_today`"""
    create_event(
        Event(
            title="Pytest_title",
            description="Pytest_description",
            location="Pytest_location",
            full_day=False,
            date="2022-11-20",
            start_time="2022-11-20T16:30:00+01:00",
            end_time="2022-11-20T17:30:00+01:00",
        )
    )
