import datetime
import json
import os
import sys
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from sys import platform

import pandas as pd
from loguru import logger
from pandas.errors import IndexingError

from aswe.core.use_case import GeneralUseCase
from aswe.core.user_interaction import SpeechToText, TextToSpeech


def clear_shell() -> None:
    """Clears any previous text in the shell"""
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        os.system("clear")
    elif platform == "win32":
        os.system("cls")


@dataclass
class User:
    """Dataclass supposed to store the user data

    Parameters
    ----------
    name : str | None
        The name of the user. _By default `None`_.
    age : int | None
        The age of the user. _By default `None`_.
    street : str | None
        The street of the user. _By default `None`_.
    city : str | None
        The city of the user. _By default `None`_.
    zip_code : int | None
        The zip code of the user. _By default `None`_.
    country : str | None
        The country of the user. _By default `None`_.
    """

    name: str | None = None
    age: int | None = None
    street: str | None = None
    city: str | None = None
    zip_code: int | None = None
    county: str | None = None


class Agent:
    """Class to handle speech to text conversion and text to speech conversion

    * TODO: Reevaluate naming for `self.tts.convert_text` and `self.stt.convert_speech`
    """

    def __init__(self, get_mic_index: bool = False) -> None:
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

        self.stt = SpeechToText(get_mic_index)
        self.tts = TextToSpeech()

        self.uc_general = GeneralUseCase(self.stt, self.tts)

        self.assistant_name = "Marcell J'Avais"
        self.user = User()

    def _greeting(self) -> None:
        """Function to greet the user."""
        hour = datetime.datetime.now().hour

        if 4 <= hour < 12:
            greeting_text = "Good Morning."
        elif 12 <= hour < 18:
            greeting_text = "Good Afternoon."
        else:
            greeting_text = "Good Evening."

        self.tts.convert_text(greeting_text)
        self.tts.convert_text(f"I am your Assistant {self.assistant_name}")

    def _get_user(self) -> None:
        """Asks for the name of the user."""
        self.tts.convert_text("What should i call you?")

        username = None
        while username is None:
            print("")
            username = self.stt.convert_speech()
            if username is None:
                self.tts.convert_text("Sorry, I didn't get that. Please say that again.")

        self.user.name = username  # type: ignore
        self.tts.convert_text(f"Hello {self.user.name}")
        self.tts.convert_text("How can I help you?")

    def _get_best_match(self, text: str) -> tuple[str, str] | None:
        """Find the best match for the parsed text

        * TODO: Switch from text to speech input for multiple use cases

        Parameters
        ----------
        text : str
            _description_

        Returns
        -------
        tuple[str, str]
            _description_
        """
        logger.debug(f"Finding the best match for the parsed text: {text}")
        logger.debug(f"The data frame contains {len(self.quotes)} rows")
        temp_df: pd.DataFrame = self.quotes.copy()

        try:
            temp_df["similarity"] = temp_df["phrase"].apply(
                lambda value: SequenceMatcher(None, text, value).quick_ratio()
            )
            temp_df = temp_df.iloc[
                temp_df.groupby(["use_case", "choice"], sort=False)["similarity"].agg(pd.Series.idxmax)
            ]
            temp_df = temp_df[temp_df["similarity"] >= 0.5].reset_index(drop=True)
            temp_df = temp_df.loc[temp_df["similarity"] == temp_df["similarity"].max()]
        except ValueError:
            logger.warning("Could not find a match for the parsed text meeting the requirements.")
            return None
        except KeyError:
            logger.error("The data frame does not match the required schema.")
            return None
        except IndexingError:
            logger.error("The data frame does not match the required schema.")
            return None

        if temp_df.empty:
            return None

        choice = 0
        if len(temp_df) > 1:
            print("")
            self.tts.convert_text("I got multiple matches. Please choose one.")
            print("")
            for index, row in temp_df.iterrows():
                print(f"{index + 1}: {row['use_case']}, {row['choice']}")  # type: ignore
            print("")
            while choice == 0:
                try:
                    choice = int(input("Please enter the number of your choice: "))
                except ValueError:
                    self.tts.convert_text("Sorry, I didn't get that. Please try again.")

        selected_row = temp_df.iloc[choice - 1 if len(temp_df) > 1 else 0]
        return (selected_row["use_case"], selected_row["choice"])

    def agent(self) -> None:
        """Main function to interact with the user

        * TODO: Get user data by console or attributes
        """
        clear_shell()
        self._greeting()
        self._get_user()

        while True:
            print("")
            query = self.stt.convert_speech()
            if not query:
                self.tts.convert_text(
                    "Sorry, I was not able to parse anything. If you said something, please try again."
                )
                continue
            parsed_text = query.lower()
            self.evaluate_use_case(parsed_text)

    def evaluate_use_case(self, text: str) -> None:
        """Evaluates the parsed text to trigger the correct use case

        * TODO: Implement more use cases
        * TODO: Add method for calculating the similarity between the parsed text and the use case

        Parameters
        ----------
        text : str
            The voice input of the user parsed to lower case string
        """
        logger.debug(f"Evaluating the parsed text: {text}")

        df_best_match = self._get_best_match(text)
        if df_best_match is None:
            self.tts.convert_text("Sorry, I didn't find a match for your request.")
            return None

        if df_best_match[0] == "general":
            self.uc_general.evaluate_text(df_best_match[1])
        elif df_best_match[0] == "morningBriefing":
            raise NotImplementedError
        elif df_best_match[0] == "events":
            raise NotImplementedError
        elif df_best_match[0] == "transportation":
            raise NotImplementedError
        else:
            self.tts.convert_text(
                "I was not able to map your input to a use case. Maybe the request is not implemented yet."
            )


# class UseCases:
#     """Lorem Ipsum"""

#     def evaluate_use_case(self, parsed_text: str) -> None:
#         """Lorem Ipsum"""
# All the commands said by user will be
# stored here in 'query' and will be
# converted to lower case for easily
# recognition of command
# if "wikipedia" in query:
#     speak("Searching Wikipedia...")
#     query = query.replace("wikipedia", "")
#     results = wikipedia.summary(query, sentences=3)
#     speak("According to Wikipedia")
#     print(results)
#     speak(results)

# if "how are you" in parsed_text:
#     self.tts.convert_text("I am fine, Thank you")
#     self.tts.convert_text("How are you?")

# elif "change name" in parsed_text:
#     self.tts.convert_text("What would you like to call me? ")

#     temp = self.stt.convert_speech()
#     if temp is None:
#         logger.warning("No name was given")
#     if temp:
#         self.assistant_name = temp

#     self.tts.convert_text("Thanks for naming me")

# elif "what's your name" in parsed_text or "What is your name" in parsed_text:
#     self.tts.convert_text("My friends call me")
#     self.tts.convert_text(self.assistant_name)
#     print("My friends call me", self.assistant_name)

# elif "joke" in query:
#     speak(pyjokes.get_joke())

# elif "calculate" in query:

#     app_id = "Wolframalpha api id"
#     client = wolframalpha.Client(app_id)
#     indx = query.lower().split().index("calculate")
#     query = query.split()[indx + 1 :]
#     res = client.query(" ".join(query))
#     answer = next(res.results).text
#     print("The answer is " + answer)
#     speak("The answer is " + answer)

# elif "who i am" in parsed_text:
#     self.tts.convert_text("If you talk then definitely your human.")

# elif "who are you" in parsed_text:
#     self.tts.convert_text("I am your virtual assistant")

# elif "don't listen" in parsed_text or "stop listening" in parsed_text:
#     self.tts.convert_text(f"for how much time you want to stop {self.assistant_name} from listening commands")

#     temp = self.stt.convert_speech()
#     a = int(temp if temp is not None else 60)
#     time.sleep(a)
#     print(a)

# elif "jarvis" in parsed_text:
#     self.tts.convert_text(f"{self.assistant_name} in your service Mister")

# elif "weather" in parsed_text:

#     # Google Open weather website
#     # to get API of Open weather
#     api_key = "Api key"
#     base_url = "http://api.openweathermap.org / data / 2.5 / weather?"
#     speak(" City name ")
#     print("City name : ")
#     city_name = self.stt.convert_speech()
#     complete_url = base_url + "appid =" + api_key + "&q =" + city_name
#     response = requests.get(complete_url)
#     x = response.json()

#     if x["code"] != "404":
#         y = x["main"]
#         current_temperature = y["temp"]
#         current_pressure = y["pressure"]
#         current_humidiy = y["humidity"]
#         z = x["weather"]
#         weather_description = z[0]["description"]
#         print(
#             " Temperature (in kelvin unit) = "
#             + str(current_temperature)
#             + "\n atmospheric pressure (in hPa unit) ="
#             + str(current_pressure)
#             + "\n humidity (in percentage) = "
#             + str(current_humidiy)
#             + "\n description = "
#             + str(weather_description)
#         )

#     else:
#         speak(" City Not Found ")

# elif "Good Morning" in parsed_text:
#     self.tts.convert_text("A warm" + parsed_text)
#     self.tts.convert_text("How are you Mister")
#     self.tts.convert_text(self.assistant_name)

# most asked question from google Assistant
# elif "will you be my gf" in parsed_text or "will you be my bf" in parsed_text:
#     self.tts.convert_text("I'm not sure about, may be you should give me some time")

# elif "how are you" in parsed_text:
#     self.tts.convert_text("I'm fine, glad you me that")

# elif "i love you" in parsed_text:
#     self.tts.convert_text("It's hard to understand")


if __name__ == "__main__":
    # TODO: Add args
    agent = Agent()
    agent.agent()
