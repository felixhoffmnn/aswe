from pathlib import Path

import speech_recognition as sr
from pyttsx3 import Engine

from aswe.core.user_interaction import SpeechToText, TextToSpeech


def test_convert_file() -> None:
    """Test if the speech is parsed correctly"""
    audio_path = Path("data/test_user_interaction.wav")
    stt = SpeechToText(microphone_index=-1)
    assert isinstance(stt, SpeechToText)
    assert isinstance(stt.recognizer, sr.Recognizer)

    parsed_text = stt.convert_audio_file(audio_path)
    assert isinstance(parsed_text, str)
    assert parsed_text == "this is a test for the text to speech conversion"


def test_convert_text() -> None:
    """Test if text is parsed without any errors."""
    tts = TextToSpeech()
    assert isinstance(tts, TextToSpeech)
    assert isinstance(tts.engine, Engine)

    tts.convert_text("This is a test for the text to speech conversion.")
