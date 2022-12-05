import sys
import time
from datetime import datetime

import pyjokes

from aswe.core.objects import BestMatch
from aswe.utils.abstract import AbstractUseCase


class GeneralUseCase(AbstractUseCase):
    """Class for managing the general use case"""

    def check_proactivity(self) -> None:
        """Check if there is a proactivity to be triggered

        * TODO: Implement proactivity
        """
        raise NotImplementedError

    def trigger_assistant(self, best_match: BestMatch) -> None:
        """UseCase for general questions

        The general use case aims to answer general questions like the most popular
        ones asked Google assistant. This use case also includes the option to exit
        the assistant.

        * TODO: Exit confirmation does not work

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
                if self.user.age >= 18:
                    self.tts.convert_text(pyjokes.get_joke())
                else:
                    self.tts.convert_text("Sorry, I am not allowed to tell jokes to minors.")
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
