from abc import ABC, abstractmethod

from aswe.core.objects import BestMatch, User
from aswe.core.user_interaction import SpeechToText, TextToSpeech


class AbstractUseCase(ABC):
    """Abstract class for use cases"""

    def __init__(self, stt: SpeechToText, tts: TextToSpeech, assistant_name: str, user: User) -> None:
        """Use case constructor to provide objects from the parent agent class

        * TODO: Add Attributes section
        * TODO: Change how we pass arguments to the constructor/functions

        Parameters
        ----------
        stt : SpeechToText
            The speech to text object
        tts : TextToSpeech
            The text to speech object
        assistant_name : str
            The name of the assistant
        user: User
            User preference information
        """
        self.stt = stt
        self.tts = tts
        self.assistant_name = assistant_name
        self.user = user

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
        raise NotImplementedError
