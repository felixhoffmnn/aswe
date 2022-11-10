import datetime
import json
import os
import sys
import time
from dataclasses import dataclass
from itertools import chain
from pathlib import Path
from sys import platform

import pyttsx3
import speech_recognition as sr
from loguru import logger

from aswe.core.use_case import uc_general
from aswe.utils.speech_text import speech_to_text, text_to_speech


def clear_shell() -> None:
    """Clears any previous text in the shell"""
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        os.system("clear")
    elif platform == "win32":
        os.system("cls")


@dataclass
class User:
    """Dataclass supposed to store the user data"""

    name: str
    age: int
    street: str
    city: str
    county: str


class Agent:
    """Class to handle speech to text conversion and text to speech conversion"""

    def __init__(self) -> None:
        try:
            with open(Path("data/use_case/quotes.json"), encoding="utf-8") as file:
                self.quotes = json.load(file)
        except OSError:
            logger.error("Could not open file. Please check if the file exists.")
            sys.exit(1)

        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.use_case = UseCases(self.engine, self.recognizer)

        self.assistant_name = "Marcell J'Avais"
        self.user_name = "User"

    def _greeting(self) -> None:
        """Function to greet the user

        * TODO: Discuss if this should be moved to the UseCases class
        """
        hour = datetime.datetime.now().hour

        if 4 <= hour < 12:
            text_to_speech("Good Morning!", self.engine)
        elif 12 <= hour < 18:
            text_to_speech("Good Afternoon!", self.engine)
        else:
            text_to_speech("Good Evening!", self.engine)

        text_to_speech(f"I am your Assistant {self.assistant_name}", self.engine)

    def _username(self) -> None:
        """Asks for the name of the user

        * TODO: Discuss if this should be moved to the UseCases class
        """
        text_to_speech("What should i call you sir", self.engine)

        temp = speech_to_text(self.recognizer)
        self.user_name = temp if temp else "User"
        text_to_speech(f"Hello {self.user_name}", self.engine)

        print("\n#####################\n")
        print(f"Hello {self.user_name}")
        print("\n#####################\n")

        text_to_speech("How can i Help you!", self.engine)

    def hi_buddy(self) -> None:
        """Main function to interact with the user"""
        clear_shell()
        self._greeting()
        self._username()

        while True:
            query = speech_to_text(self.recognizer)

            if query:
                parsed_text = query.lower()
                self.use_case.evaluate_use_case(parsed_text)

    def evaluate_use_case(self, text: str) -> None:
        """Evaluates the parsed text to trigger the correct use case

        * TODO: Implement more use cases

        Parameters
        ----------
        text : str
            The voice input of the user parsed to lower case string
        """
        logger.debug(f"UseCases.evaluate_use_case({text})")

        response: str | None = None
        if text in list(chain.from_iterable(self.quotes["general"].values())):
            response = uc_general(text, self.quotes["general"])
        if response:
            text_to_speech(response, self.engine)


class UseCases:
    """Lorem Ipsum"""

    def __init__(self, engine: pyttsx3.Engine, recognizer: sr.Recognizer) -> None:
        self.engine = engine
        self.recognizer = recognizer

    def evaluate_use_case(self, parsed_text: str) -> None:
        """Lorem Ipsum"""
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

        if "how are you" in parsed_text:
            text_to_speech("I am fine, Thank you", self.engine)
            text_to_speech("How are you, Sir", self.engine)

        elif "change name" in parsed_text:
            text_to_speech("What would you like to call me, Sir ", self.engine)

            temp = speech_to_text(self.recognizer)
            if temp is None:
                logger.warning("No name was given")
            if temp:
                self.assistant_name = temp

            text_to_speech("Thanks for naming me", self.engine)

        elif "what's your name" in parsed_text or "What is your name" in parsed_text:
            text_to_speech("My friends call me", self.engine)
            text_to_speech(self.assistant_name, self.engine)
            print("My friends call me", self.assistant_name)

        elif "exit" in parsed_text:
            text_to_speech("Thanks for giving me your time", self.engine)
            exit()

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
        #     text_to_speech("If you talk then definitely your human.", self.engine)

        elif "is love" in parsed_text:
            text_to_speech("It is 7th sense that destroy all other senses", self.engine)

        # elif "who are you" in parsed_text:
        #     text_to_speech("I am your virtual assistant", self.engine)

        elif "don't listen" in parsed_text or "stop listening" in parsed_text:
            text_to_speech(
                f"for how much time you want to stop {self.assistant_name} from listening commands", self.engine
            )

            temp = speech_to_text(self.recognizer)
            a = int(temp if temp is not None else 60)
            time.sleep(a)
            print(a)

        # elif "jarvis" in parsed_text:
        #     text_to_speech(f"{self.assistant_name} in your service Mister", self.engine)

        # elif "weather" in parsed_text:

        #     # Google Open weather website
        #     # to get API of Open weather
        #     api_key = "Api key"
        #     base_url = "http://api.openweathermap.org / data / 2.5 / weather?"
        #     speak(" City name ")
        #     print("City name : ")
        #     city_name = speech_to_text()
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
        #     text_to_speech("A warm" + parsed_text, self.engine)
        #     text_to_speech("How are you Mister", self.engine)
        #     text_to_speech(self.assistant_name, self.engine)

        # most asked question from google Assistant
        # elif "will you be my gf" in parsed_text or "will you be my bf" in parsed_text:
        #     text_to_speech("I'm not sure about, may be you should give me some time", self.engine)

        # elif "how are you" in parsed_text:
        #     text_to_speech("I'm fine, glad you me that", self.engine)

        # elif "i love you" in parsed_text:
        #     text_to_speech("It's hard to understand", self.engine)


if __name__ == "__main__":
    agent = Agent()
    agent.hi_buddy()
