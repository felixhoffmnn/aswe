from abc import ABC, abstractmethod

from aswe.core.objects import BestMatch, User
from aswe.core.user_interaction import SpeechToText, TextToSpeech


class AbstractUseCase(ABC):
    """Abstract class for use cases"""

    def __init__(self, stt: SpeechToText, tts: TextToSpeech, assistant_name: str, user: User) -> None:
        """Use case constructor to provide objects from the parent agent class

        * TODO: Add Attributes section

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
        """Abstract method for use case classes

        Handles business logic and communication between user and apis depending on user input.

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

    @abstractmethod
    def check_proactivity(self) -> None:
        """Abstract method for use case classes

        Checks apis if certain events have occurred and informs user.

        Raises
        ------
        NotImplementedError
            If the given key was not found in the match case statement for implemented functions,
            or if the function is not implemented yet.
        """
        raise NotImplementedError
