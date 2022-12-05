# pylint: disable=no-value-for-parameter
import pytest

from aswe.api.calendar.data import Event


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
