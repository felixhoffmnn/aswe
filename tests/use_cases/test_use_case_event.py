# ? Disable private attribute access to test class methods
# pylint: disable=redefined-outer-name,protected-access

import pytest
from googlemaps import Client
from pytest_mock import MockFixture

from aswe.api.calendar.data import Event
from aswe.api.event.event import EventApi
from aswe.api.weather.weather import WeatherApi
from aswe.core.objects import Address, BestMatch, Possessions, User
from aswe.core.user_interaction import SpeechToText, TextToSpeech
from aswe.use_cases.event import EventUseCase


@pytest.fixture(scope="function")
def patch_stt(mocker: MockFixture) -> SpeechToText:
    """Patch `convert_speech` method of `SpeechToText` Class"""
    patched_stt: SpeechToText = mocker.patch.object(SpeechToText, "convert_speech")

    return patched_stt


@pytest.fixture(scope="function")
def patch_tts(mocker: MockFixture) -> TextToSpeech:
    """Patch `convert_text` method of `TextToSpeech` Class"""
    patched_tts: TextToSpeech = mocker.patch.object(TextToSpeech, "convert_text")

    return patched_tts


def test_this_weekend_no_events(mocker: MockFixture, patch_stt: SpeechToText, patch_tts: TextToSpeech) -> None:
    """Test "thisWeekend" event of `use_cases.event`, when no event is returned.

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    patch_stt : SpeechToText
        Patched class to instantiate use_case class
    patch_tts : TextToSpeech
        Patched class to instantiate use_case class
    """

    best_match = BestMatch(use_case="events", function_key="thisWeekend", similarity=1, parsed_text="lorem ipsum")
    user = User(
        name="TestUser",
        age=10,
        address=Address(street="Pfaffenwaldring 45", city="Stuttgart", zip_code=70569, country="DE", vvs_id=""),
        possessions=Possessions(bike=True, car=False),
        favorite_stocks=[],
    )
    use_case = EventUseCase(patch_stt, patch_tts, "TestBuddy", user)

    # * Patch Event Api
    mocked_event_api = mocker.patch.object(EventApi, "events", return_value=None)

    # * Spy on tts.convert_text
    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")

    use_case.trigger_assistant(best_match)

    spy_tts_convert_text.assert_called_once_with("Looks like there are no events this weekend.")
    mocked_event_api.assert_called_once()


def test_this_weekend_one_attendable_event(
    mocker: MockFixture, patch_stt: SpeechToText, patch_tts: TextToSpeech
) -> None:
    """Test "thisWeekend" event of `use_cases.event`, when one event is returned.

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    patch_stt : SpeechToText
        Patched class to instantiate use_case class
    patch_tts : TextToSpeech
        Patched class to instantiate use_case class
    """

    best_match = BestMatch(use_case="events", function_key="thisWeekend", similarity=1, parsed_text="lorem ipsum")
    user = User(
        name="TestUser",
        age=10,
        address=Address(street="Pfaffenwaldring 45", city="Stuttgart", zip_code=70569, country="DE", vvs_id=""),
        possessions=Possessions(bike=True, car=False),
        favorite_stocks=[],
    )
    use_case = EventUseCase(patch_stt, patch_tts, "TestBuddy", user)

    # * Patch Event Api
    test_events = [
        {
            "id": "test_id",
            "name": "test_name",
            "start": "2030-01-01T00:00:00Z",
            "status": "onsale",
            "location": {"name": "test_location_name", "city": "test_city", "address": "test_address"},
        }
    ]

    mocked_event_api = mocker.patch.object(EventApi, "events", return_value=test_events)

    # * Patch Calendar Api
    test_calendar_events = [
        Event(
            title="test_calendar_event",
            description="",
            location="Stuttgart",
            full_day=False,
            date="2030-01-01",
            start_time="2030-01-01T20:00:00",
            end_time="2030-01-01T21:00:00",
        )
    ]

    # mocked_calendar_api = mocker.patch.object(calendar, "get_events_by_timeframe", return_value=test_calendar_events)
    mocker.patch("aswe.use_cases.event.get_events_by_timeframe", return_value=test_calendar_events)

    # * Patch Weather Api
    test_weather_response = {"days": [{"hours": [{"temp": 4, "precipprob": 50}]}]}

    mocked_weater_api = mocker.patch.object(WeatherApi, "forecast", return_value=test_weather_response)

    # * Patch googlemaps Api
    test_directions_response = [{"legs": [{"duration": {"text": "test min"}}]}]

    mocked_google_maps_api = mocker.patch.object(Client, "directions", return_value=test_directions_response)

    # * Spy on tts.convert_text
    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")

    use_case.trigger_assistant(best_match)

    mocked_event_api.assert_called_once()
    mocked_weater_api.assert_called_once()
    mocked_google_maps_api.assert_called_once()
    assert spy_tts_convert_text.call_count == 5
