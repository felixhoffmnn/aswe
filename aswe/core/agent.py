import json
import sys
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path

import pandas as pd
from fire import Fire
from loguru import logger
from pandas.errors import IndexingError

from aswe.core.data import BestMatch, User
from aswe.core.use_case import GeneralUseCase
from aswe.core.user_interaction import SpeechToText, TextToSpeech
from aswe.utils.general import clear_shell


class Agent:
    """Class to handle speech to handle main functionality of the assistant

    The core functionality of the assistant is to handle speech-to-text conversion (_stt_), text-to_speech (_tts_)
    conversion, calculate the best match for the parsed text, greet the user, trigger the right use case,
    and handle proactivity.
    """

    def __init__(self, get_mic: bool = False, get_user: bool = False, is_test: bool = False) -> None:
        """
        * TODO: Add Attributes section
        * TODO: Tokenize the phrases and input

        Parameters
        ----------
        get_mic : bool, optional
            Boolean if the speech to text class should first ask for the microphone to use. _By default `False`_.
        get_user : bool, optional
            Boolean if the default user should be used. _By default `False`_.
        is_test : bool, optional
            Boolean if the agent is used for testing. _By default `False`_.

        Attributes
        ----------
        assistant_name : str
            The name of the assistant
        is_test : bool
            Boolean if the agent is used for testing
        quotes : pd.DataFrame
            DataFrame storing the use cases and functionality combinations
        stt : SpeechToText
            Speech to text class to handle speech-to-text conversion
        tts : TextToSpeech
            Text to speech class to handle text-to-speech conversion
        user : User
            User class to store the user information (eg., name, age)
        uc_general : GeneralUseCase
            General use case class to handle general use cases
        """
        self.assistant_name = "HiBuddy"

        try:
            with open(Path("data/quotes.json"), encoding="utf-8") as file:
                self.quotes = (
                    pd.DataFrame(
                        [
                            [use_case, choice, phrase]
                            for use_case, value in json.load(file).items()
                            for choice, phrase in value.items()
                        ],
                        columns=["use_case", "choice", "phrase"],
                    )
                    .explode("phrase")
                    .reset_index(drop=True)
                )
        except OSError:
            logger.error("Could not open file. Please check if the file exists.")
            sys.exit(1)

        self.stt = SpeechToText(get_mic, is_test)
        self.tts = TextToSpeech(is_test)

        if get_user:
            clear_shell()
            self.user = self._get_user()
        else:
            self.user = User(name="Felix", age=22)

        self.uc_general = GeneralUseCase(self.stt, self.tts, self.assistant_name)

    def _greeting(self) -> None:
        """Function to greet the user."""
        hour = datetime.now().hour

        if 4 <= hour < 12:
            greeting_text = f"Good Morning {self.user.name}."
        elif 12 <= hour < 18:
            greeting_text = f"Good Afternoon {self.user.name}."
        else:
            greeting_text = f"Good Evening {self.user.name}."

        self.tts.convert_text(greeting_text)
        self.tts.convert_text(f"I am your Assistant {self.assistant_name}")
        self.tts.convert_text("How can I help you?")

    def _get_user(self) -> User:
        """Asks for the name of the user.

        * TODO: Refactor into a util function
        """
        name = input("What is your name? ")

        age = None
        while age is None:
            try:
                age = int(input("What is your age? "))
            except ValueError:
                print("Please enter a valid age.")

        return User(name=name)  # type: ignore

    def get_best_match(self, parsed_text: str, threshold: float = 0.5) -> BestMatch | None:
        """Find the best match for the parsed text

        Function calculates the similarity between the parsed text and the use cases.

        * TODO: Add tokenization and stop words

        ??? example "`self.quotes` DataFrame"

            The `self.quotes` consists of three columns: `use_case`, `choice` and `phrase`.
            We use the `use_case` and `choice` column for the chain-of-responsibility pattern
            to map the best match to the final function. The `phrase` column contains multiple phrases
            which are going to be compared to the parsed text.

            |     | use_case        | choice       | phrase                    |
            | --- | --------------- | ------------ | ------------------------- |
            | 0   | morningBriefing | newsSummary  | whats going on            |
            | 1   | morningBriefing | newsSummary  | morning briefing          |
            | 2   | events          | eventSummary | what is going on          |
            | 3   | transportation  | dhbw         | dhbw                      |
            | 4   | transportation  | dhbw         | i need to get to the dhbw |
            | 5   | transportation  | hpe          | i need to get to the hpe  |

        Parameters
        ----------
        parsed_text : str
            The parsed text which should be matched to a use case.
        threshold : float, optional
            The threshold which is used to determine if the similarity is high enough to be considered.
            The value needs to be between 0 and 1. _By default `0.5`_.

        Raises
        ------
        ValueError
            If the threshold is not between 0 and 1.

        Returns
        -------
        BestMatch
            Returns a object with the use case, the selected endpoint within the use case (choice),
            the similarity, and the parsed text.
        """
        logger.debug(f"Finding the best match for the parsed text: {parsed_text}")
        logger.debug(f"The data frame contains {len(self.quotes)} rows")
        if threshold < 0 or threshold > 1:
            raise ValueError("The threshold needs to be between 0 and 1.")

        temp_df: pd.DataFrame = self.quotes.copy()

        try:
            temp_df["similarity"] = temp_df["phrase"].apply(
                lambda value: SequenceMatcher(None, parsed_text, value).quick_ratio()
            )
            temp_df = temp_df.iloc[
                temp_df.groupby(["use_case", "choice"], sort=False)["similarity"].agg(pd.Series.idxmax)
            ]
            temp_df = temp_df[temp_df["similarity"] >= threshold].reset_index(drop=True)
            temp_df = temp_df.loc[temp_df["similarity"] == temp_df["similarity"].max()]
        except ValueError:
            logger.warning("Could not find a match for the parsed text meeting the requirements.")
            return None
        except (KeyError, IndexingError):
            logger.error("The data frame does not match the required schema.")
            return None

        if temp_df.empty:
            return None

        choice = None
        if len(temp_df) > 1:
            print("")
            self.tts.convert_text("I got multiple matches. Please choose one.")
            print("")
            for index, row in temp_df.iterrows():
                print(f"{index}: {row['use_case']}, {row['choice']}")
            print("")
            while choice is None:
                try:
                    choice = int(input("Please enter the number of your choice: "))
                except ValueError:
                    self.tts.convert_text("Sorry, I didn't get that. Please try again.")

        selected_row = temp_df.iloc[choice if choice else 0]
        return BestMatch(
            selected_row["use_case"],
            selected_row["choice"],
            selected_row["similarity"],
            parsed_text,
        )

    def check_proactivity(self) -> None:
        """Checks if there are any updates which should be announced to the user

        * TODO: Implement proactivity
        """
        # Call use_case_1.proactive()
        logger.debug("Checking for proactivity.")

    def agent(self) -> None:
        """Main function to interact with the user

        The agent function is the main function of the assistant. It first greets the user and
        then checks proactively if there are updates for the user. If thats not the case, it will start
        listening for user input in `60` second intervals. If the user input is not empty, it will
        execute the use case function for proactivity.
        """
        clear_shell()
        self._greeting()
        proactivity_last_checked = datetime.now().minute

        while True:
            print("")

            # TODO: Implement proactivity
            if proactivity_last_checked % 15 == 0:
                self.check_proactivity()

            query = self.stt.convert_speech()
            if not query:
                self.tts.convert_text(
                    "Sorry, I was not able to parse anything. If you said something, please try again."
                )
                continue
            parsed_text = query.lower()
            self.evaluate_use_case(parsed_text)

    def evaluate_use_case(self, parsed_text: str) -> None:
        """Evaluates the parsed text to trigger the correct use case

        * TODO: Implement more use cases

        Parameters
        ----------
        parsed_text : str
            The voice input of the user parsed to lower case string
        """
        logger.info(f"Evaluating the parsed text: {parsed_text}")

        best_match = self.get_best_match(parsed_text)
        if best_match is None:
            self.tts.convert_text("Sorry, I didn't find a match for your request.")
            return None

        logger.info(best_match)

        try:
            match best_match.use_case:
                case "general":
                    self.uc_general.trigger_assistant(best_match)
                case "morningBriefing":
                    raise NotImplementedError
                case "events":
                    raise NotImplementedError
                case "transportation":
                    raise NotImplementedError
                case "sport":
                    raise NotImplementedError
                case _:
                    self.tts.convert_text(
                        "I was not able to map your input to a use case. Maybe the request is not implemented yet."
                    )
        except NotImplementedError:
            self.tts.convert_text("Sorry, the requested function is not implemented yet.")

        return None


if __name__ == "__main__":
    Fire(Agent)
