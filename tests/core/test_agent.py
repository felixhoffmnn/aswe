# pylint: disable=redefined-outer-name,protected-access
import json
from pathlib import Path

import pytest

from aswe.core.agent import Agent
from aswe.core.objects import User
from aswe.core.user_interaction import SpeechToText, TextToSpeech


@pytest.fixture
def agent() -> Agent:
    """Patch `convert_text` method of `TextToSpeech` Class"""
    return Agent()


def test_init(agent: Agent) -> None:
    """Test agent initialization"""
    assert isinstance(agent, Agent)

    assert agent.assistant_name == "HiBuddy"

    with open(Path("data/quotes.json"), encoding="utf-8") as file:
        combinations = [len(phrase) for _, value in json.load(file).items() for _, phrase in value.items()]
    assert len(agent.quotes["phrase"]) == sum(combinations)

    assert isinstance(agent.user, User)
    assert isinstance(agent.stt, SpeechToText)
    assert isinstance(agent.tts, TextToSpeech)
