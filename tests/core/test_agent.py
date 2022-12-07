# pylint: disable=redefined-outer-name,protected-access
import json
from pathlib import Path

import pytest

from aswe.core.agent import Agent
from aswe.core.objects import BestMatch, User
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


def test_greeting(agent: Agent) -> None:
    """Test agent greeting"""

    agent._greeting()


def test_evaluate_use_case(agent: Agent) -> None:
    """Test agent evaluate_use_case and get_best_match"""

    agent._evaluate_use_case("marry me")


def test_check_proactivity(agent: Agent) -> None:
    """Test agent check_proactivity"""

    agent._check_proactivity()
