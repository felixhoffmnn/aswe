import sys
from abc import ABC
from datetime import datetime

from loguru import logger

from aswe.core.user_interaction import SpeechToText, TextToSpeech


class AbstractUseCase(ABC):
    """Abstract class for use cases"""

    def __init__(self, stt: SpeechToText, tts: TextToSpeech) -> None:
        self.stt = stt
        self.tts = tts


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

    def evaluate_text(self, choice: str) -> None:
        """UseCase for general questions

        Parameters
        ----------
        choice : str
            The best matching choice for the given user input.
        """
        if choice == "time":
            logger.debug(f"General Use Case: {choice}")
            current_time = datetime.now().strftime("%H:%M")
            self.tts.convert_text(f"The current time is {current_time}")
        elif choice == "wellBeing":
            self.tts.convert_text("I am fine, Thank you")
        elif choice == "exit":
            self.tts.convert_text("Do you really want to exit?")
            response = self.stt.convert_speech()
            if response in ["yes", "yeah", "yep", "sure", "ok"]:
                self.tts.convert_text("Thanks for using me, have a nice day.")
                sys.exit()
