# pylint: disable=redefined-outer-name

from datetime import datetime

import pytest
from pytest_mock import MockFixture

from aswe.core.objects import Address, BestMatch, Favorites, Possessions, User
from aswe.core.user_interaction import SpeechToText, TextToSpeech
from aswe.use_cases.navigation import NavigationUseCase


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


@pytest.mark.xfail(raises=FileNotFoundError, reason="The token file is not available")
def test_proactivity(patch_stt: SpeechToText, patch_tts: TextToSpeech) -> None:
    """Test proactivity of `use_cases.navigation`.

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    patch_stt : SpeechToText
        Patched class to instantiate use_case class
    patch_tts : TextToSpeech
        Patched class to instantiate use_case class
    """

    user = User(
        name="TestUser",
        age=10,
        address=Address(street="Pfaffenwaldring 45", city="Stuttgart", zip_code=70569, country="DE", vvs_id=""),
        possessions=Possessions(bike=True, car=True),
        favorites=Favorites(
            stocks=[],
            league="",
            team="",
            news_country="",
            news_keywords=[""],
            wakeup_time=datetime.now(),
        ),
    )
    use_case = NavigationUseCase(patch_stt, patch_tts, "TestBuddy", user)

    use_case.check_proactivity()


@pytest.mark.xfail(raises=FileNotFoundError, reason="The token file is not available")
def test_dhbw(mocker: MockFixture, patch_stt: SpeechToText, patch_tts: TextToSpeech) -> None:
    """Test "dhbw" event of `use_cases.navigation`.

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    patch_stt : SpeechToText
        Patched class to instantiate use_case class
    patch_tts : TextToSpeech
        Patched class to instantiate use_case class
    """

    best_match = BestMatch(use_case="navigation", function_key="dhbw", similarity=1, parsed_text="lorem ipsum")
    user = User(
        name="TestUser",
        age=10,
        address=Address(street="Pfaffenwaldring 45", city="Stuttgart", zip_code=70569, country="DE", vvs_id=""),
        possessions=Possessions(bike=True, car=True),
        favorites=Favorites(
            stocks=[],
            league="",
            team="",
            news_country="",
            news_keywords=[""],
            wakeup_time=datetime.now(),
        ),
    )
    use_case = NavigationUseCase(patch_stt, patch_tts, "TestBuddy", user)

    # * Spy on tts.convert_text
    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")

    use_case.trigger_assistant(best_match)

    spy_tts_convert_text.assert_called_once()


@pytest.mark.xfail(raises=FileNotFoundError, reason="The token file is not available")
def test_hpe(mocker: MockFixture, patch_stt: SpeechToText, patch_tts: TextToSpeech) -> None:
    """Test "hpe" event of `use_cases.navigation`.

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    patch_stt : SpeechToText
        Patched class to instantiate use_case class
    patch_tts : TextToSpeech
        Patched class to instantiate use_case class
    """

    best_match = BestMatch(use_case="navigation", function_key="hpe", similarity=1, parsed_text="lorem ipsum")
    user = User(
        name="TestUser",
        age=10,
        address=Address(street="Pfaffenwaldring 45", city="Stuttgart", zip_code=70569, country="DE", vvs_id=""),
        possessions=Possessions(bike=True, car=True),
        favorites=Favorites(
            stocks=[],
            league="",
            team="",
            news_country="",
            news_keywords=[""],
            wakeup_time=datetime.now(),
        ),
    )
    use_case = NavigationUseCase(patch_stt, patch_tts, "TestBuddy", user)

    # * Spy on tts.convert_text
    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")

    use_case.trigger_assistant(best_match)

    spy_tts_convert_text.assert_called_once()


@pytest.mark.xfail(raises=FileNotFoundError, reason="The token file is not available")
def test_ibm(mocker: MockFixture, patch_stt: SpeechToText, patch_tts: TextToSpeech) -> None:
    """Test "ibm" event of `use_cases.navigation`.

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    patch_stt : SpeechToText
        Patched class to instantiate use_case class
    patch_tts : TextToSpeech
        Patched class to instantiate use_case class
    """

    best_match = BestMatch(use_case="navigation", function_key="ibm", similarity=1, parsed_text="lorem ipsum")
    user = User(
        name="TestUser",
        age=10,
        address=Address(street="Pfaffenwaldring 45", city="Stuttgart", zip_code=70569, country="DE", vvs_id=""),
        possessions=Possessions(bike=True, car=True),
        favorites=Favorites(
            stocks=[],
            league="",
            team="",
            news_country="",
            news_keywords=[""],
            wakeup_time=datetime.now(),
        ),
    )
    use_case = NavigationUseCase(patch_stt, patch_tts, "TestBuddy", user)

    # * Spy on tts.convert_text
    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")

    use_case.trigger_assistant(best_match)

    spy_tts_convert_text.assert_called_once()


@pytest.mark.xfail(raises=FileNotFoundError, reason="The token file is not available")
def test_next_event(mocker: MockFixture, patch_stt: SpeechToText, patch_tts: TextToSpeech) -> None:
    """Test "nextEvent" event of `use_cases.navigation`.

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    patch_stt : SpeechToText
        Patched class to instantiate use_case class
    patch_tts : TextToSpeech
        Patched class to instantiate use_case class
    """

    best_match = BestMatch(use_case="navigation", function_key="nextEvent", similarity=1, parsed_text="lorem ipsum")
    user = User(
        name="TestUser",
        age=10,
        address=Address(street="Pfaffenwaldring 45", city="Stuttgart", zip_code=70569, country="DE", vvs_id=""),
        possessions=Possessions(bike=True, car=True),
        favorites=Favorites(
            stocks=[],
            league="",
            team="",
            news_country="",
            news_keywords=[""],
            wakeup_time=datetime.now(),
        ),
    )
    use_case = NavigationUseCase(patch_stt, patch_tts, "TestBuddy", user)

    # * Spy on tts.convert_text
    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")

    use_case.trigger_assistant(best_match)

    spy_tts_convert_text.assert_called_once()
