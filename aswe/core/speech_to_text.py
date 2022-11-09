import datetime
import os
import time
import webbrowser
from sys import platform

import pyttsx3
import speech_recognition as sr
from loguru import logger

from aswe.utils.speech_text import speech_to_text, text_to_speech

# import requests
# import random
# from urllib.request import urlopen
# import ctypes
# import json
# import shutil
# import smtplib
# import winshell
# from bs4 import BeautifulSoup
# import tkinter
# import operator
# import wikipedia
# import pyjokes
# import feedparser
# import wolframalpha
# from twilio.rest import Client
# from clint.textui import progress
# from ecapture import ecapture as ec


def clear_shell() -> None:
    """Clears any previous text in the shell"""
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        os.system("clear")
    elif platform == "win32":
        os.system("cls")


class Wrapper:
    """Class to handle speech to text conversion and text to speech conversion"""

    def __init__(self) -> None:
        self.engine = pyttsx3.init("espeak")
        self.recognizer = sr.Recognizer()
        self.use_case = UseCases(self.engine, self.recognizer)

        self.assistant_name = "Jarvis"
        self.user_name = "User"

    def _greeting(self) -> None:
        """Function to greet the user"""
        hour = int(datetime.datetime.now().hour)

        if hour >= 0 and hour < 12:
            text_to_speech("Good Morning!", self.engine)
        elif hour >= 12 and hour < 18:
            text_to_speech("Good Afternoon!", self.engine)
        else:
            text_to_speech("Good Evening!", self.engine)

        text_to_speech(f"I am your Assistant {self.assistant_name}", self.engine)

    def _username(self) -> None:
        """Asks for the name of the user"""
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


choice = {
    "morning briefing": {
        1: "whats going on",
        2: "morning briefing",
    },
    "events": {
        1: "events",
    },
    "transportation": {
        1: "train",
        2: "bus",
        3: "car",
        4: "bike",
    },
}


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

        if "open youtube" in parsed_text:
            text_to_speech("Here you go to Youtube\n", self.engine)
            webbrowser.open("youtube.com")

        elif "open google" in parsed_text:
            text_to_speech("Here you go to Google\n", self.engine)
            webbrowser.open("google.com")

        elif "open stackoverflow" in parsed_text:
            text_to_speech("Here you go to Stack Over flow.Happy coding", self.engine)
            webbrowser.open("stackoverflow.com")

        elif "the time" in parsed_text:
            strTime = datetime.datetime.now().strftime("% H:% M:% S")
            text_to_speech(f"Sir, the time is {strTime}", self.engine)

        elif "how are you" in parsed_text:
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

        elif "search" in parsed_text or "play" in parsed_text:

            parsed_text = parsed_text.replace("search", "")
            parsed_text = parsed_text.replace("play", "")
            webbrowser.open(parsed_text)

        # elif "who i am" in parsed_text:
        #     text_to_speech("If you talk then definitely your human.", self.engine)

        # elif "why you came to world" in parsed_text:
        #     text_to_speech("Thanks to Gaurav. further It's a secret", self.engine)

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

        elif "where is" in parsed_text:
            parsed_text = parsed_text.replace("where is", "")
            location = parsed_text
            text_to_speech("User asked to Locate", self.engine)
            text_to_speech(location, self.engine)
            webbrowser.open("https://www.google.nl / maps / place/" + location + "")

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
    wrapper = Wrapper()
    wrapper.hi_buddy()
