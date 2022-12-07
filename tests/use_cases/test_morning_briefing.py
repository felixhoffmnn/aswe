# ? Disable private attribute access to test class methods
# pylint: disable=redefined-outer-name,protected-access

from datetime import datetime
from unittest.mock import call

import pytest
from pytest_mock import MockFixture

from aswe.api.calendar import Event
from aswe.core.objects import Address, BestMatch, Favorites, Possessions, User
from aswe.core.user_interaction import SpeechToText, TextToSpeech
from aswe.use_cases.morning_briefing import MorningBriefingUseCase


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


@pytest.fixture()
def patch_use_case(patch_stt: SpeechToText, patch_tts: TextToSpeech) -> MorningBriefingUseCase:
    """Patch `MorningBriefingUseCase` instance

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
        address=Address(street="Pfaffenwaldring 45", city="Stuttgart", zip_code=70569, country="Germany", vvs_id=""),
        possessions=Possessions(bike=True, car=False),
        favorites=Favorites(
            stocks=[{"name": "Apple", "symbol": "AAPL"}],
            league="",
            team="",
            news_country="Australia",
            news_keywords=[""],
            wakeup_time=datetime.now(),
        ),
    )
    return MorningBriefingUseCase(patch_stt, patch_tts, "TestBuddy", user)


def test_full_briefing(mocker: MockFixture, patch_tts: TextToSpeech, patch_use_case: MorningBriefingUseCase) -> None:
    """Test "full_briefing" event of `use_cases.morning_briefing`.
    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    patch_stt : SpeechToText
        Patched class to instantiate use_case class
    patch_tts : TextToSpeech
        Patched class to instantiate use_case class
    """

    best_match = BestMatch(
        use_case="morningBriefing", function_key="fullBriefing", similarity=1, parsed_text="lore ipsum"
    )
    mocker.patch("aswe.use_cases.morning_briefing.MorningBriefingUseCase._calendar_overview")
    mocker.patch("aswe.use_cases.morning_briefing.MorningBriefingUseCase._news_overview")
    mocker.patch("aswe.use_cases.morning_briefing.MorningBriefingUseCase._weather_overview")
    mocker.patch("aswe.use_cases.morning_briefing.MorningBriefingUseCase._finance_overview")
    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")

    patch_use_case.trigger_assistant(best_match)

    assert spy_tts_convert_text.call_args_list == [
        call(
            "Good morning TestUser! It's time to get up! Here is your morning briefing "
            "providing all the essential information to start into the day."
        ),
        call("Now about your calendar:"),
        call("Let me give you a quick overview about some important news:"),
        call("Now let's have a look at the weather forecast:"),
        call("And finally, here are some information about your stocks:"),
        call("That was everything for today. Have a nice day!"),
    ]


def test_calendar_overview(
    mocker: MockFixture, patch_tts: TextToSpeech, patch_use_case: MorningBriefingUseCase
) -> None:
    """Test "calendar_overview" event of `use_cases.morning_briefing`.
    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    patch_stt : SpeechToText
        Patched class to instantiate use_case class
    patch_tts : TextToSpeech
        Patched class to instantiate use_case class
    """

    best_match = BestMatch(use_case="morningBriefing", function_key="calendar", similarity=1, parsed_text="lore ipsum")

    # Regular event
    calendar_event = Event(
        title="test_calendar_event",
        description="",
        location="Stuttgart",
        full_day=False,
        date="2030-01-01",
        start_time="2030-01-01T20:00:00+01:00",
        end_time="2030-01-01T21:00:00+01:00",
    )
    mocker.patch("aswe.use_cases.morning_briefing.get_all_events_today", return_value=[calendar_event])
    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")

    patch_use_case.trigger_assistant(best_match)

    assert spy_tts_convert_text.call_args_list == [
        call("Today you have the following calendar events:"),
        call("test_calendar_event at Stuttgart from 20:00 to 21:00"),
    ]

    # Withouth location and full day
    calendar_event = Event(
        title="test_calendar_event",
        description="",
        location="",
        full_day=True,
        date="2030-01-01",
        start_time="2030-01-01T20:00:00+01:00",
        end_time="2030-01-01T21:00:00+01:00",
    )
    mocker.patch("aswe.use_cases.morning_briefing.get_all_events_today", return_value=[calendar_event])
    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")

    patch_use_case.trigger_assistant(best_match)

    assert spy_tts_convert_text.call_args_list == [
        call("Today you have the following calendar events:"),
        call("test_calendar_event all day"),
    ]

    # Test with no event
    mocker.patch("aswe.use_cases.morning_briefing.get_all_events_today", return_value=[])
    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")

    patch_use_case.trigger_assistant(best_match)

    spy_tts_convert_text.assert_called_once_with("You do not have any calendar events today.")


def test_news_overview(mocker: MockFixture, patch_tts: TextToSpeech, patch_use_case: MorningBriefingUseCase) -> None:
    """Test "news_overview" event of `use_cases.morning_briefing`.
    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    patch_stt : SpeechToText
        Patched class to instantiate use_case class
    patch_tts : TextToSpeech
        Patched class to instantiate use_case class
    """

    best_match = BestMatch(use_case="morningBriefing", function_key="news", similarity=1, parsed_text="lore ipsum")

    country_top_headlines = ["Title 1: Description 1"]
    keyword_top_headlines = ["Title 2: Description 2"]
    mocker.patch("aswe.use_cases.morning_briefing.top_headlines_search", return_value=country_top_headlines)
    mocker.patch("aswe.use_cases.morning_briefing.keyword_search", return_value=keyword_top_headlines)
    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")

    patch_use_case.trigger_assistant(best_match)

    assert spy_tts_convert_text.call_args_list == [
        call("These are the top headlines in your country:"),
        call("Title 1: Description 1"),
        call("You could also be interested in these headlines:"),
        call("Title 2: Description 2"),
    ]

    # Test with no headlines at all
    mocker.patch("aswe.use_cases.morning_briefing.top_headlines_search", return_value=None)
    mocker.patch("aswe.use_cases.morning_briefing.keyword_search", return_value=None)
    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")

    patch_use_case.trigger_assistant(best_match)

    spy_tts_convert_text.assert_called_once_with("Unfortunately, I could not find any news for you today.")


def test_weather_overview(mocker: MockFixture, patch_tts: TextToSpeech, patch_use_case: MorningBriefingUseCase) -> None:
    """Test "weather_overview" event of `use_cases.morning_briefing`.
    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    patch_stt : SpeechToText
        Patched class to instantiate use_case class
    patch_tts : TextToSpeech
        Patched class to instantiate use_case class
    """

    best_match = BestMatch(use_case="morningBriefing", function_key="weather", similarity=1, parsed_text="lore ipsum")

    weather_response = {
        "days": [
            {
                "sunrise": "06:00:00",
                "sunset": "18:00:00",
                "temp": 5.5,
                "tempmin": 3.5,
                "tempmax": 7.5,
                "feelslike": 4.5,
                "precipprob": 50,
            }
        ]
    }
    mocker.patch("aswe.use_cases.morning_briefing.dynamic_range", return_value=weather_response)
    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")

    patch_use_case.trigger_assistant(best_match)

    spy_tts_convert_text.assert_called_once_with(
        """Today it will be 5.5 degrees Celsius (with a minimum of """
        """3.5 and a maximum of 7.5). This feels """
        """like 4.5 degrees. The probability of precipitation is """
        """50 percent. The sun will rise at 06:00 and set at 18:00."""
    )

    # Test with no weather data
    mocker.patch("aswe.use_cases.morning_briefing.dynamic_range", return_value=None)
    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")

    patch_use_case.trigger_assistant(best_match)

    spy_tts_convert_text.assert_called_once_with(
        "Unfortunately, I could not find any weather information for you today."
    )


def test_finance_overview(mocker: MockFixture, patch_tts: TextToSpeech, patch_use_case: MorningBriefingUseCase) -> None:
    """Test "finance_overview" event of `use_cases.morning_briefing`.
    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    patch_stt : SpeechToText
        Patched class to instantiate use_case class
    patch_tts : TextToSpeech
        Patched class to instantiate use_case class
    """

    best_match = BestMatch(use_case="morningBriefing", function_key="finance", similarity=1, parsed_text="lore ipsum")

    stock_price = 120.96
    stock_price_change = {
        "24h": "-1.92%",
        "5D": "+3.86%",
    }
    stock_rating = "S minus (Strong Buy)"
    mocker.patch("aswe.use_cases.morning_briefing.get_stock_price", return_value=stock_price)
    mocker.patch("aswe.use_cases.morning_briefing.get_stock_price_change", return_value=stock_price_change)
    mocker.patch("aswe.use_cases.morning_briefing.get_stock_rating", return_value=stock_rating)
    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")

    patch_use_case.trigger_assistant(best_match)

    assert spy_tts_convert_text.call_args_list == [
        call("About Apple:"),
        call("The Apple stock is currently trading at 120.96 Euro per share."),
        call("It has changed by -1.92% in the last 24 hours (+3.86% in the last 5 days)."),
        call("The latest rating by analysts is S minus (Strong Buy)."),
    ]

    # Test with no stock data
    mocker.patch("aswe.use_cases.morning_briefing.get_stock_price", return_value=None)
    mocker.patch("aswe.use_cases.morning_briefing.get_stock_price_change", return_value=None)
    mocker.patch("aswe.use_cases.morning_briefing.get_stock_rating", return_value=None)
    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")

    patch_use_case.trigger_assistant(best_match)

    spy_tts_convert_text.assert_called_once_with("Unfortunately, I could not find any information for you today.")
