from aswe.api.calendar.calendar import (
    get_all_events_today,
    get_events_by_timeframe,
    get_next_event_today,
)
from aswe.api.calendar.data import Event


def test_get_events_by_timeframe() -> None:
    """Test `aswe.api.calendar.calendar.get_events_by_timeframe`"""
    events = get_events_by_timeframe("2022-10-19T00:00:00.000001Z", "2022-10-19T23:59:59.999999Z")

    assert isinstance(events, list)
    assert len(events) == 4
    assert isinstance(events[0], Event)
    assert isinstance(events[1], Event)
    assert isinstance(events[2], Event)
    assert isinstance(events[3], Event)


def test_get_all_events_today() -> None:
    """Test `aswe.api.calendar.calendar.get_all_events_today`"""
    events = get_all_events_today()

    assert isinstance(events, list)


def test_get_next_event_today() -> None:
    """Test `aswe.api.calendar.calendar.get_next_event_today`"""
    event = get_next_event_today()

    assert event is None or isinstance(event, Event)


# def test_create_event() -> None:
#     """Test `aswe.api.calendar.calendar.get_next_event_today`"""
#     try:
#         create_event(
#             Event(
#                 title="Pytest_title",
#                 description="Pytest_description",
#                 location="Pytest_location",
#                 full_day=False,
#                 date="2022-11-20",
#                 start_time="2022-11-20T16:30:00+01:00",
#                 end_time="2022-11-20T17:30:00+01:00",
#             )
#         )
#     except Exception:
#         assert False
