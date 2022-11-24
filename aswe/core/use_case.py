import sys
import time
from abc import ABC, abstractmethod
from datetime import datetime

import pyjokes
from loguru import logger

from aswe.core.user_interaction import SpeechToText, TextToSpeech


class AbstractUseCase(ABC):
    """Abstract class for use cases"""

    def __init__(self, stt: SpeechToText, tts: TextToSpeech, assistant_name: str) -> None:
        """Use case constructor to provide objects from the parent agent class

        Parameters
        ----------
        stt : SpeechToText
            The speech to text object
        tts : TextToSpeech
            The text to speech object
        assistant_name : str
            The name of the assistant
        """
        self.stt = stt
        self.tts = tts
        self.assistant_name = assistant_name

    @abstractmethod
    def trigger_assistant(self, quotes_key: str) -> None:
        """UseCase for morning briefing

        Parameters
        ----------
        quotes_key : str
            The best matching key for the given user input.
        """


class MorningBriefingUseCase(AbstractUseCase):
    """ "Use case for the morning briefing"""

    def trigger_assistant(self, quotes_key: str) -> None:
        """UseCase for morning briefing

        * TODO: Implement `quotes_key`

        Parameters
        ----------
        quotes_key : str
            The best matching key for the given user input.
        """
        if quotes_key == "newsSummary":
            raise NotImplementedError

        else:
            raise NotImplementedError


class SportUseCase(AbstractUseCase):
    """ "Use case for sports"""

    def trigger_assistant(self, quotes_key: str) -> None:
        """UseCase for sport

        * TODO: Implement `quotes_key`

        Parameters
        ----------
        quotes_key : str
            The best matching key for the given user input.
        """
        if quotes_key == "newsSummary":
            raise NotImplementedError

        else:
            raise NotImplementedError


class EventUseCase(AbstractUseCase):
    """Use case to handle events"""

    def trigger_assistant(self, quotes_key: str) -> None:
        """UseCase for events

        * TODO: Implement `quotes_key`

        Parameters
        ----------
        quotes_key : str
            The best matching key for the given user input.
        """
        if quotes_key == "eventSummary":
            raise NotImplementedError

        else:
            raise NotImplementedError


class TransportationUseCase(AbstractUseCase):
    """Use case for transportation"""

    def trigger_assistant(self, quotes_key: str) -> None:
        """UseCase for transportation

        * TODO: Implement `quotes_key`

        Parameters
        ----------
        quotes_key : str
            The best matching key for the given user input.
        """
        if quotes_key == "dhbw":
            raise NotImplementedError

        elif quotes_key == "hpw":
            raise NotImplementedError

        elif quotes_key == "ibm":
            raise NotImplementedError

        else:
            raise NotImplementedError


class GeneralUseCase(AbstractUseCase):
    """Class for managing the general use case"""

    def trigger_assistant(self, quotes_key: str) -> None:
        """UseCase for general questions

        Parameters
        ----------
        quotes_key : str
            The best matching key for the given user input.
        """
        if quotes_key == "time":
            logger.debug(f"General Use Case: {quotes_key}")
            current_time = datetime.now().strftime("%H:%M")
            self.tts.convert_text(f"The current time is {current_time}")

        elif quotes_key == "wellBeing":
            self.tts.convert_text("I am fine, Thank you")

        elif quotes_key == "name":
            self.tts.convert_text("I am your digital assistant")
            self.tts.convert_text(f"Most of the time I am being called {self.assistant_name}")

        elif quotes_key == "joke":
            self.tts.convert_text(pyjokes.get_joke())

        elif quotes_key == "stopListening":
            self.tts.convert_text("For how long do you want me to stop listening (in seconds)?")

            sleep_time = 0
            while sleep_time == 0:
                try:
                    sleep_time = int(input("Please enter the number of your choice: "))
                except ValueError:
                    self.tts.convert_text("Sorry, I didn't get that. Please try again.")

            time.sleep(sleep_time)
            self.tts.convert_text("I am back again.")

        elif quotes_key == "marryMe":
            self.tts.convert_text("I am sorry, I am already married to my job.")

        elif quotes_key == "boyGirlFriend":
            self.tts.convert_text("I am sorry, I am not interested in any relationship with my customers.")

        elif quotes_key == "exit":
            self.tts.convert_text("Do you really want to exit?")
            response = self.stt.convert_speech()
            if response in ["yes", "yeah", "yep", "sure", "ok"]:
                self.tts.convert_text("Thanks for using me, have a nice day.")
                sys.exit()

        else:
            raise NotImplementedError
