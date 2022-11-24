import sys
import time
from abc import ABC, abstractmethod
from datetime import datetime

import pyjokes

from aswe.core.data import BestMatch
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
    def trigger_assistant(self, best_match: BestMatch) -> None:
        """UseCase for morning briefing

        Parameters
        ----------
        best_match : BestMatch
            An object containing the best match for the user input.

        Raises
        ------
        NotImplementedError
            If the given key was not found in the match case statement for implemented functions,
            or if the function is not implemented yet.
        """


class MorningBriefingUseCase(AbstractUseCase):
    """ "Use case for the morning briefing"""

    def trigger_assistant(self, best_match: BestMatch) -> None:
        """UseCase for morning briefing

        * TODO: Implement `quotes_key`

        Parameters
        ----------
        best_match : BestMatch
            An object containing the best match for the user input.

        Raises
        ------
        NotImplementedError
            If the given key was not found in the match case statement for implemented functions,
            or if the function is not implemented yet.
        """
        match best_match.function_key:
            case "newsSummary":
                raise NotImplementedError
            case _:
                raise NotImplementedError


class SportUseCase(AbstractUseCase):
    """ "Use case for sports"""

    def trigger_assistant(self, best_match: BestMatch) -> None:
        """UseCase for sport

        * TODO: Implement `quotes_key`

        Parameters
        ----------
        best_match : BestMatch
            An object containing the best match for the user input.

        Raises
        ------
        NotImplementedError
            If the given key was not found in the match case statement for implemented functions,
            or if the function is not implemented yet.
        """
        match best_match.function_key:
            case "sportSummary":
                raise NotImplementedError
            case _:
                raise NotImplementedError


class EventUseCase(AbstractUseCase):
    """Use case to handle events"""

    def trigger_assistant(self, best_match: BestMatch) -> None:
        """UseCase for events

        * TODO: Implement `quotes_key`

        Parameters
        ----------
        best_match : BestMatch
            An object containing the best match for the user input.

        Raises
        ------
        NotImplementedError
            If the given key was not found in the match case statement for implemented functions,
            or if the function is not implemented yet.
        """
        match best_match.function_key:
            case "eventSummary":
                raise NotImplementedError
            case _:
                raise NotImplementedError


class TransportationUseCase(AbstractUseCase):
    """Use case for transportation"""

    def trigger_assistant(self, best_match: BestMatch) -> None:
        """UseCase for transportation

        * TODO: Implement `quotes_key`

        Parameters
        ----------
        best_match : BestMatch
            An object containing the best match for the user input.

        Raises
        ------
        NotImplementedError
            If the given key was not found in the match case statement for implemented functions,
            or if the function is not implemented yet.
        """
        match best_match.function_key:
            case "dhbw":
                raise NotImplementedError
            case "hpe":
                raise NotImplementedError
            case "ibm":
                raise NotImplementedError
            case _:
                raise NotImplementedError


class GeneralUseCase(AbstractUseCase):
    """Class for managing the general use case"""

    def trigger_assistant(self, best_match: BestMatch) -> None:
        """UseCase for general questions

        The general use case aims to answer general questions like the most popular
        ones asked Google assistant. This use case also includes the option to exit
        the assistant.

        Parameters
        ----------
        best_match : BestMatch
            The best matching key for the given user input.

        Raises
        ------
        NotImplementedError
            If the given key was not found in the match case statement for implemented functions,
            or if the function is not implemented yet.
        """
        match best_match.function_key:
            case "time":
                current_time = datetime.now().strftime("%H:%M")
                self.tts.convert_text(f"The current time is {current_time}")
            case "wellBeing":
                self.tts.convert_text("I am fine, Thank you")
            case "name":
                self.tts.convert_text("I am your digital assistant")
                self.tts.convert_text(f"Most of the time I am being called {self.assistant_name}")
            case "joke":
                self.tts.convert_text(pyjokes.get_joke())
            case "stopListening":
                self.tts.convert_text("For how long do you want me to stop listening (in seconds)?")

                sleep_time = 0
                while sleep_time == 0:
                    try:
                        sleep_time = int(input("Please enter the number of your choice: "))
                    except ValueError:
                        self.tts.convert_text("Sorry, I didn't get that. Please try again.")

                time.sleep(sleep_time)
                self.tts.convert_text("I am back again.")
            case "marryMe":
                self.tts.convert_text("I am sorry, I am already married to my job.")
            case "boyGirlFriend":
                self.tts.convert_text("I am sorry, I am not interested in any relationship with my customers.")
            case "exit":
                self.tts.convert_text("Do you really want to exit?")
                response = self.stt.convert_speech()
                if response in ["yes", "yeah", "yep", "sure", "ok"]:
                    self.tts.convert_text("Thanks for using me, have a nice day.")
                    sys.exit()
            case _:
                raise NotImplementedError
