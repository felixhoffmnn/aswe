# ? Disable private attribute access to test class methods
# pylint: disable=redefined-outer-name,protected-access

from datetime import datetime
from unittest.mock import call

import pytest
from pytest_mock import MockFixture

from aswe.api.calendar.data import Event
from aswe.api.event.event_data import EventLocation, EventSummary, ReducedEvent
from aswe.api.navigation.trip_data import MapsTrip
from aswe.core.objects import Address, BestMatch, Favorites, Possessions, User
from aswe.core.user_interaction import SpeechToText, TextToSpeech
from aswe.use_cases.event import EventUseCase


@pytest.fixture()
def patch_stt(mocker: MockFixture) -> SpeechToText:
    """Patch `convert_speech` method of `SpeechToText` Class"""
    patched_stt: SpeechToText = mocker.patch.object(SpeechToText, "convert_speech")

    return patched_stt


@pytest.fixture()
def patch_tts(mocker: MockFixture) -> TextToSpeech:
    """Patch `convert_text` method of `TextToSpeech` Class"""
    patched_tts: TextToSpeech = mocker.patch.object(TextToSpeech, "convert_text")

    return patched_tts


@pytest.fixture()
def patch_use_case(patch_stt: SpeechToText, patch_tts: TextToSpeech) -> EventUseCase:
    """Patch `EventUseCase` instance

    Parameters
    ----------
    patch_stt : SpeechToText
        `SpeechToText` instance with patched `convert_speech` method.
    patch_tts : TextToSpeech
        `TextToSpeech` instance with patched `convert_text` method.

    Returns
    -------
    EventUseCase
        Returns `EventUseCase` instance with patched methods
    """
    user = User(
        name="TestUser",
        age=10,
        address=Address(street="Pfaffenwaldring 45", city="Stuttgart", zip_code=70569, country="DE", vvs_id=""),
        possessions=Possessions(bike=True, car=False),
        favorites=Favorites(
            stocks=[],
            league="",
            team="",
            news_keywords=[""],
            wakeup_time=datetime.now(),
        ),
    )
    return EventUseCase(patch_stt, patch_tts, "TestBuddy", user)


def test_trigger_assistant(mocker: MockFixture, patch_tts: TextToSpeech, patch_use_case: EventUseCase) -> None:
    """Test `EventUseCase.trigger_assistant`

    Parameters
    ----------
    mocker : MockFixture
    patch_tts : TextToSpeech
        `TextToSpeech` instance with patched `convert_text` method.
    patch_use_case : EventUseCase
        `EventUseCase` instance with patched `TextToSpeech` and `SpeechToText` instances.
    """

    best_match = BestMatch(use_case="events", function_key="thisWeekend", similarity=1, parsed_text="lorem ipsum")

    reduced_events = ReducedEvent(
        id="test_id",
        name="test_name",
        start="2030-01-01T00:00:00Z",
        status="onsale",
        location=EventLocation(name="test_location_name", city="test_city", address="test_address"),
    )

    calendar_event = Event(
        title="test_calendar_event",
        description="",
        location="Stuttgart",
        full_day=False,
        date="2030-01-01",
        start_time="2030-01-01T20:00:00",
        end_time="2030-01-01T21:00:00",
    )

    event_location = EventLocation(city="test_city", address="test_address")

    event_summary = EventSummary(
        name="event_1",
        start=datetime(2030, 1, 1, 0, 0, 0),
        location=event_location,
        is_cold=True,
        is_rainy=True,
        trip_duration=10,
    )

    # ! uncomment if create_event method is added in event use case
    # mocker.patch("aswe.use_cases.event.create_event", return_value=None)

    mocker.patch("aswe.use_cases.event.get_events_by_timeframe", return_value=[calendar_event])
    mocker.patch.object(patch_use_case, "_format_event_summary", return_value="mocked_summary")
    mocker.patch.object(patch_use_case.stt, "check_if_yes", return_value=True)

    # * Test for one event
    mocked_event_api = mocker.patch.object(
        patch_use_case, "_get_events_in_preferred_city", return_value=[reduced_events]
    )
    mocker.patch.object(patch_use_case, "_get_attendable_events", return_value=[event_summary])
    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")

    patch_use_case.trigger_assistant(best_match)

    mocked_event_api.assert_called_once()
    assert spy_tts_convert_text.call_args_list == [
        call("There is one events you might want to attend to."),
        call("mocked_summary"),
        call("Do you want to attend?"),
        call("Great, the event was added to your calendar."),
    ]

    # * Test for multiple events
    mocker.patch.object(patch_use_case, "_get_attendable_events", return_value=[event_summary, event_summary])
    mocked_event_api.reset_mock()
    spy_tts_convert_text.reset_mock()

    patch_use_case.trigger_assistant(best_match)

    mocked_event_api.assert_called_once()
    assert spy_tts_convert_text.call_args_list == [
        call("There are multiple events you might want to attend to."),
        call("mocked_summary"),
        call("Do you want to attend?"),
        call("Great, the event was added to your calendar."),
        call("mocked_summary"),
        call("Do you want to attend?"),
        call("Great, the event was added to your calendar."),
    ]

    # * Test for one event
    mocker.patch.object(patch_use_case, "_get_attendable_events", return_value=[])
    mocked_event_api.reset_mock()
    spy_tts_convert_text.reset_mock()

    patch_use_case.trigger_assistant(best_match)

    mocked_event_api.assert_called_once()
    assert spy_tts_convert_text.call_args_list == [
        call("There are no events this weekend that fit your weekend plans.")
    ]


def test_get_attendable_events(mocker: MockFixture, patch_use_case: EventUseCase) -> None:
    """Test `EventUseCase._get_attendable_events`

    Parameters
    ----------
    mocker : MockFixture
    patch_use_case : EventUseCase
        `EventUseCase` instance with patched `TextToSpeech` and `SpeechToText` instances.
    """
    event_location = EventLocation(city="test_city", address="test_address")
    reduced_event = ReducedEvent(
        id="test_id", name="test_name", start="2030-01-01T03:00:00Z", status="test_status", location=event_location
    )
    calendar_event = Event(
        title="test_title",
        description="",
        location="test_location",
        full_day=False,
        date="",
        start_time="2030-01-01T00:00:00+01:00",
        end_time="2030-01-01T03:00:00+01:00",
    )
    event_summary = EventSummary(
        name="event_1",
        start=datetime(2030, 1, 1, 0, 0, 0),
        location=event_location,
        is_cold=True,
        is_rainy=True,
        trip_duration=10,
    )

    mocker.patch.object(patch_use_case, "_event_is_attendable", return_value=True)
    mocker.patch.object(patch_use_case, "_get_event_summary", return_value=event_summary)

    assert patch_use_case._get_attendable_events([reduced_event], [calendar_event]) == [event_summary]


def test_event_is_attendable(mocker: MockFixture, patch_use_case: EventUseCase) -> None:
    """Test `EventUseCase._event_is_attendable`

    Parameters
    ----------
    mocker : MockFixture
    patch_use_case : EventUseCase
        `EventUseCase` instance with patched `TextToSpeech` and `SpeechToText` instances.
    """
    event_location = EventLocation(city="test_city", address="test_address")
    reduced_event = ReducedEvent(
        id="test_id", name="test_name", start="2030-01-01T03:00:00Z", status="test_status", location=event_location
    )

    calendar_event_1 = Event(
        title="test_title",
        description="",
        location="test_location",
        full_day=False,
        date="",
        start_time="2030-01-01T00:00:00+01:00",
        end_time="2030-01-01T03:00:00+01:00",
    )

    calendar_event_2 = Event(
        title="test_title",
        description="",
        location="test_location",
        full_day=True,
        date="2030-01-01",
        start_time="",
        end_time="",
    )

    mocker.patch.object(
        patch_use_case,
        "_get_event_times",
        return_value=(datetime.strptime(reduced_event.start, "%Y-%m-%dT%H:%M:%SZ"), None),
    )

    assert patch_use_case._event_is_attendable(reduced_event, [calendar_event_1]) is False
    assert patch_use_case._event_is_attendable(reduced_event, [calendar_event_2]) is True


def test_get_event_summary(mocker: MockFixture, patch_use_case: EventUseCase) -> None:
    """Test `EventUseCase._get_event_summary`
    Parameters
    ----------
    mocker : MockFixture
    patch_use_case : EventUseCase
        `EventUseCase` instance with patched `TextToSpeech` and `SpeechToText` instances.
    """

    event_location = EventLocation(city="test_city", address="test_address")
    reduced_event = ReducedEvent(
        id="test_id", name="test_name", start="2030-01-01T00:00:00Z", status="test_status", location=event_location
    )

    mocker.patch.object(
        patch_use_case,
        "_get_event_times",
        return_value=(datetime.strptime(reduced_event.start, "%Y-%m-%dT%H:%M:%SZ"), None),
    )

    mocked_forecast_response = {"days": [{"hours": [{"temp": 10, "precipprob": 20}]}]}
    mocker.patch("aswe.use_cases.event.weatherApi.forecast", return_value=mocked_forecast_response)

    mocked_trip_response = MapsTrip(duration=20, distance=10)
    mocker.patch("aswe.use_cases.event.get_maps_connection", return_value=mocked_trip_response)

    expected_event_summary = EventSummary(
        name="test_name",
        start=datetime.strptime(reduced_event.start, "%Y-%m-%dT%H:%M:%SZ"),
        location=event_location,
        is_cold=False,
        is_rainy=False,
        trip_duration=20,
    )

    assert expected_event_summary == patch_use_case._get_event_summary(reduced_event)


def test_get_event_times(patch_use_case: EventUseCase) -> None:
    """Test `EventUseCase._get_event_times`

    Parameters
    ----------
    patch_use_case : EventUseCase
        `EventUseCase` instance with patched `TextToSpeech` and `SpeechToText` instances.
    """
    event_location = EventLocation(city="test_city", address="test_address", name="test_name")
    reduced_event = ReducedEvent(
        id="test_id", name="test_name", start="2030-01-01T00:00:00Z", status="test_status", location=event_location
    )

    (event_start_datetime, event_end_datetime) = patch_use_case._get_event_times(reduced_event, event_duration=2)
    assert (event_end_datetime - event_start_datetime).seconds / (60 * 60) == 2

    (event_start_datetime, event_end_datetime) = patch_use_case._get_event_times(reduced_event, event_duration=4)
    assert (event_end_datetime - event_start_datetime).seconds / (60 * 60) == 4


def test_format_event_summary(patch_use_case: EventUseCase) -> None:
    """Test `EventUseCase._format_event_summary`

    Parameters
    ----------
    patch_use_case : EventUseCase
        `EventUseCase` instance with patched `TextToSpeech` and `SpeechToText` instances.
    """
    event_location = EventLocation(city="test_city", address="test_address", name="test_name")
    event_summary_1 = EventSummary(
        name="event_1",
        start=datetime(2030, 1, 1, 0, 0, 0),
        location=event_location,
        is_cold=True,
        is_rainy=True,
        trip_duration=10,
    )

    event_summary_2 = EventSummary(
        name="event_2",
        start=datetime(2030, 1, 1, 0, 0, 0),
        location=event_location,
        is_cold=False,
        is_rainy=False,
        trip_duration=10,
    )

    assert patch_use_case._format_event_summary(event_summary_1) == (
        "The event_1 starts at 00:00. It will take you 10 minutes to get there by bike. "
        "There is a high chance of rain, you might want to take an umbrella. "
        "Additionally, you should prepare for chilly temperatures."
    )

    assert patch_use_case._format_event_summary(event_summary_2) == (
        "The event_2 starts at 00:00. It will take you 10 minutes to get there by bike. "
    )
