import sys
from abc import ABC
from datetime import datetime

from loguru import logger

from aswe.core.speech_text import SpeechToText, TextToSpeech


class AbstractUseCase(ABC):
    """Abstract class for use cases"""

    def __init__(self, stt: SpeechToText, tts: TextToSpeech, quotes: dict[str, list[str]]) -> None:
        self.stt = stt
        self.tts = tts
        self.quotes = quotes


# def uc_morning_briefing(parsed_text: str, quotes: dict[str, list[str]]) -> None:
#     """Lorem Ipsum

#     * TODO: Implement
#     """


# def uc_events(parsed_text: str, quotes: dict[str, list[str]]) -> None:
#     """Lorem Ipsum

#     * TODO: Implement
#     """


# def uc_transportation(parsed_text: str, quotes: dict[str, list[str]]) -> None:
#     """Lorem Ipsum

#     * TODO: Implement
#     """


class GeneralUseCase(AbstractUseCase):
    """Class for managing the general use case"""

    def evaluate_text(self, parsed_text: str) -> None:
        """UseCase for general questions

        Parameters
        ----------
        parsed_text : str
            The voice input of the user parsed to lower case string.
        quotes : dict[str, list[str]]
            The dictionary of quotes regarding the general use case.
        """
        if parsed_text in self.quotes["time"]:
            logger.debug(f"General Use Case: {parsed_text}, {self.quotes}, {self.quotes['time']}")
            current_time = datetime.now().strftime("%H:%M")
            self.tts.convert_text(f"The current time is {current_time}")
        elif parsed_text in self.quotes["exit"]:
            self.tts.convert_text("Thanks for using me, have a nice day.")
            sys.exit()
        elif parsed_text in self.quotes["well_being"]:
            self.tts.convert_text("I am fine, Thank you")
