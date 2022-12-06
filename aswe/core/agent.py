import json
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
from fire import Fire
from loguru import logger
from pandas.errors import IndexingError

from aswe.core.objects import Address, BestMatch, LogProactivity, Possessions, User
from aswe.core.user_interaction import SpeechToText, TextToSpeech
from aswe.use_cases import (
    EventUseCase,
    GeneralUseCase,
    SportUseCase,
    TransportationUseCase,
)
from aswe.utils.date import check_timedelta
from aswe.utils.shell import clear_shell, get_int, print_options
from aswe.utils.text import calculate_similarity


class Agent:
    """Class to handle speech to handle main functionality of the assistant

    The core functionality of the assistant is to handle speech-to-text conversion (_stt_), text-to_speech (_tts_)
    conversion, calculate the best match for the parsed text, greet the user, trigger the right use case,
    and handle proactivity.

    ```mermaid
    graph LR;

    start_agent --> greet_user;
    greet_user --> check_for_proactivity;
    check_for_proactivity --> trigger_proactivity;
    trigger_proactivity --> get_user_input;
    check_for_proactivity --> get_user_input;
    get_user_input --> calculate_best_match;
    calculate_best_match --> trigger_use_case;
    trigger_use_case --> check_for_proactivity;
    ```
    """

    def __init__(self, get_mic: bool = False) -> None:
        """
        * TODO: Add Attributes section
        * TODO: Tokenize the phrases and input
        * TODO: Add flag for triggering proactivity
        * TODO: Add variable for storing the last time when proactivity was triggered

        Parameters
        ----------
        get_mic : bool, optional
            Boolean if the speech to text class should first ask for the microphone to use. _By default `False`_.

        Attributes
        ----------
        assistant_name : str
            The name of the assistant
        quotes : pd.DataFrame
            DataFrame storing the use cases and functionality combinations
        user : User
            User class to store the user information (eg., name, age)
        stt : SpeechToText
            Speech to text class to handle speech-to-text conversion
        tts : TextToSpeech
            Text to speech class to handle text-to-speech conversion
        user : User
            User class to store the user information (eg., name, age)
        log_proactivity : LogProactivity
            Log proactivity class to handle the logging of proactivity
        uc_general : GeneralUseCase
            General use case class to handle general use cases
        uc_transportation : TransportationUseCase
            Transportation use case class to handle transportation use cases
        uc_event : EventUseCase
            Event use case class to handle event use cases
        uc_sport : SportUseCase
            Sport use case class to handle sport use cases
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

        try:
            with open(Path("data/user.json"), encoding="utf-8") as file:
                user_data = json.load(file)
                self.user = User(
                    name=user_data["name"],
                    age=user_data["age"],
                    possessions=Possessions(bike=user_data["possessions"]["bike"], car=user_data["possessions"]["car"]),
                    address=Address(
                        street=user_data["address"]["street"],
                        city=user_data["address"]["city"],
                        zip_code=user_data["address"]["zip_code"],
                        country=user_data["address"]["country"],
                        vvs_id=user_data["address"]["vvs_id"],
                    ),
                    favorite_stocks=user_data["favorite_stocks"],
                )
        except OSError:
            logger.error("Could not open file. Please check if the file exists.")
            sys.exit(1)
        except KeyError:
            logger.error("It appears that not all necessary keys are correctly set in the `user.json` file.")
            sys.exit(1)

        self.stt = SpeechToText(get_mic)
        self.tts = TextToSpeech()

        self.log_proactivity = LogProactivity()

        self.uc_general = GeneralUseCase(self.stt, self.tts, self.assistant_name, self.user)
        self.uc_transportation = TransportationUseCase(self.stt, self.tts, self.assistant_name, self.user)
        self.uc_event = EventUseCase(self.stt, self.tts, self.assistant_name, self.user)
        self.uc_sport = SportUseCase(self.stt, self.tts, self.assistant_name, self.user)

    def _greeting(self) -> None:
        """Function to greet the user."""
        hour = datetime.now().hour

        if 4 <= hour < 12:
            greeting_text = f"Good Morning {self.user.name}."
        elif 12 <= hour < 18:
            greeting_text = f"Good Afternoon {self.user.name}."
        else:
            greeting_text = f"Good Evening {self.user.name}."

        clear_shell()
        self.tts.convert_text(greeting_text)
        self.tts.convert_text(f"I am your Assistant {self.assistant_name}")
        self.tts.convert_text("How can I help you?")

    def get_best_match(self, parsed_text: str, threshold: float = 0.7) -> BestMatch | None:
        """Find the best match for the parsed text

        Function calculates the similarity between the parsed text and the use cases.

        * TODO: Add tokenization and stop words
        * TODO: Extract calculation of similarity into a util function
        * TODO: Watch if the default threshold is too high

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
            The value needs to be between 0 and 1. _By default `0.7`_.

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
            temp_df["similarity"] = temp_df["phrase"].apply(lambda value: calculate_similarity(parsed_text, value))
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
            logger.warning("Could not find a match for the parsed text meeting the requirements.")
            return None

        choice = None
        if len(temp_df) > 1:
            self.tts.convert_text("I got multiple matches. Please choose one.", line_above=True)

            options = temp_df["phrase"].tolist()
            print_options(options=options)
            choice = get_int(options=options)

        if choice is not None or len(temp_df) == 1:
            selected_row = temp_df.iloc[choice - 1 if choice is not None else 0]
            return BestMatch(
                selected_row["use_case"],
                selected_row["choice"],
                selected_row["similarity"],
                parsed_text,
            )

        return None

    def check_proactivity(self) -> None:
        """Checks if there are any updates which should be announced to the user

        For each use case the interval can be set individually. If the interval is reached
        the `check_proactivity` function of the current use case is called.

        * TODO: Implement proactivity for morning briefing
        * TODO: Add alarm function for morning briefing
        """
        logger.debug("Checking for proactivity.")

        try:
            if check_timedelta(self.log_proactivity.last_event_check, 15):
                logger.debug("Triggering proactivity for events.")
                self.uc_event.check_proactivity()
        except NotImplementedError:
            logger.warning("Proactivity for events is not implemented yet.")

        # try:
        #     if check_timedelta(self.log_proactivity.last_morning_briefing_check, 15):
        #         logger.debug("Triggering proactivity for morning briefing.")
        #         self.uc_morning_briefing.check_proactivity()
        # except NotImplementedError:
        #     logger.warning("Proactivity for morning briefing is not implemented yet.")

        try:
            if check_timedelta(self.log_proactivity.last_sport_check, 15):
                logger.debug("Triggering proactivity for sport.")
                self.uc_sport.check_proactivity()
        except NotImplementedError:
            logger.warning("Proactivity for sport is not implemented yet.")

        try:
            if check_timedelta(self.log_proactivity.last_transportation_check, 15):
                logger.debug("Triggering proactivity for transportation.")
                self.uc_transportation.check_proactivity()
        except NotImplementedError:
            logger.warning("Proactivity for transportation is not implemented yet.")

    def agent(self) -> None:
        """Main function to interact with the user

        The agent function is the main function of the assistant. It first greets the user and
        then checks proactively if there are updates for the user. If thats not the case, it will start
        listening for user input in `60` second intervals. If the user input is not empty, it will
        execute the use case function for proactivity.
        """
        self._greeting()

        while True:
            if check_timedelta(self.log_proactivity.last_check, 5):
                self.check_proactivity()

            query = self.stt.convert_speech(line_above=True)
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
                    self.uc_event.trigger_assistant(best_match)
                case "transportation":
                    self.uc_transportation.trigger_assistant(best_match)
                case "sport":
                    self.uc_sport.trigger_assistant(best_match)
                case _:
                    self.tts.convert_text(
                        "I was not able to map your input to a use case. Maybe the request is not implemented yet."
                    )
        except NotImplementedError:
            self.tts.convert_text("Sorry, the requested function is not implemented yet.")

        return None


if __name__ == "__main__":
    Fire(Agent)
