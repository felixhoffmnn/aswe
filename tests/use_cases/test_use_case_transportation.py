# pylint: disable=redefined-outer-name

import pytest
from pytest_mock import MockFixture

from aswe.core.objects import Address, BestMatch, Possessions, User
from aswe.core.user_interaction import SpeechToText, TextToSpeech
from aswe.use_cases.transportation import TransportationUseCase


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


def test_dhbw(mocker: MockFixture, patch_stt: SpeechToText, patch_tts: TextToSpeech) -> None:
    """Test "dhbw" event of `use_cases.transportation`.

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    patch_stt : SpeechToText
        Patched class to instantiate use_case class
    patch_tts : TextToSpeech
        Patched class to instantiate use_case class
    """

    best_match = BestMatch(use_case="transportation", function_key="dhbw", similarity=1, parsed_text="lorem ipsum")
    user = User(
        name="TestUser",
        age=10,
        address=Address(street="Pfaffenwaldring 45", city="Stuttgart", zip_code=70569, country="DE", vvs_id=""),
        possessions=Possessions(bike=True, car=True),
        favorite_stocks=[],
    )
    use_case = TransportationUseCase(patch_stt, patch_tts, "TestBuddy", user)

    # * Spy on tts.convert_text
    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")

    use_case.trigger_assistant(best_match)

    spy_tts_convert_text.assert_called_once()


def test_hpe(mocker: MockFixture, patch_stt: SpeechToText, patch_tts: TextToSpeech) -> None:
    """Test "hpe" event of `use_cases.transportation`.

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    patch_stt : SpeechToText
        Patched class to instantiate use_case class
    patch_tts : TextToSpeech
        Patched class to instantiate use_case class
    """

    best_match = BestMatch(use_case="transportation", function_key="hpe", similarity=1, parsed_text="lorem ipsum")
    user = User(
        name="TestUser",
        age=10,
        address=Address(street="Pfaffenwaldring 45", city="Stuttgart", zip_code=70569, country="DE", vvs_id=""),
        possessions=Possessions(bike=True, car=True),
        favorite_stocks=[],
    )
    use_case = TransportationUseCase(patch_stt, patch_tts, "TestBuddy", user)

    # * Spy on tts.convert_text
    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")

    use_case.trigger_assistant(best_match)

    spy_tts_convert_text.assert_called_once()


def test_ibm(mocker: MockFixture, patch_stt: SpeechToText, patch_tts: TextToSpeech) -> None:
    """Test "ibm" event of `use_cases.transportation`.

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    patch_stt : SpeechToText
        Patched class to instantiate use_case class
    patch_tts : TextToSpeech
        Patched class to instantiate use_case class
    """

    best_match = BestMatch(use_case="transportation", function_key="ibm", similarity=1, parsed_text="lorem ipsum")
    user = User(
        name="TestUser",
        age=10,
        address=Address(street="Pfaffenwaldring 45", city="Stuttgart", zip_code=70569, country="DE", vvs_id=""),
        possessions=Possessions(bike=True, car=True),
        favorite_stocks=[],
    )
    use_case = TransportationUseCase(patch_stt, patch_tts, "TestBuddy", user)

    # * Spy on tts.convert_text
    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")

    use_case.trigger_assistant(best_match)

    spy_tts_convert_text.assert_called_once()


def test_next_event(mocker: MockFixture, patch_stt: SpeechToText, patch_tts: TextToSpeech) -> None:
    """Test "nextEvent" event of `use_cases.transportation`.

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    patch_stt : SpeechToText
        Patched class to instantiate use_case class
    patch_tts : TextToSpeech
        Patched class to instantiate use_case class
    """

    best_match = BestMatch(use_case="transportation", function_key="nextEvent", similarity=1, parsed_text="lorem ipsum")
    user = User(
        name="TestUser",
        age=10,
        address=Address(street="Pfaffenwaldring 45", city="Stuttgart", zip_code=70569, country="DE", vvs_id=""),
        possessions=Possessions(bike=True, car=True),
        favorite_stocks=[],
    )
    use_case = TransportationUseCase(patch_stt, patch_tts, "TestBuddy", user)

    # * Spy on tts.convert_text
    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")

    use_case.trigger_assistant(best_match)

    spy_tts_convert_text.assert_called_once()
