import datetime
import os
import subprocess
import time
import webbrowser

import pyttsx3

# import requests
import speech_recognition as sr
from loguru import logger

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

engine = pyttsx3.init("espeak")
engine.setProperty("voice", "english")


def speak(text: str) -> None:
    """Converts text to speech

    Parameters
    ----------
    audio : str
        The Text which should be converted to speech
    """
    engine.say(text)
    engine.runAndWait()


def greeting() -> None:
    """Function to greet the user"""
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    bot_name = "Jarvis 1 point 0"
    speak("I am your Assistant")
    speak(bot_name)


def username() -> None:
    """Asks for the name of the user"""
    speak("What should i call you sir")
    user_name = speech_to_text()

    speak("Hello")
    if isinstance(user_name, str):
        speak(user_name)

    print("\n#####################\n")
    print(f"Hello {user_name}")
    print("\n#####################\n")

    speak("How can i Help you!")


def speech_to_text() -> str | None:
    """First records an audio file an then pareses it to text

    Returns
    -------
    str | None
        The parsed text or None if no text could be parsed
    """
    rec = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        rec.pause_threshold = 1
        audio = rec.listen(source)

    try:
        print("Recognizing...")
        parsed_text = rec.recognize_google(audio, language="en-US")
        print(f"\nUser said: {parsed_text}\n")

        if isinstance(parsed_text, str):
            return parsed_text
    except sr.UnknownValueError:
        logger.error("UnknownValueError")
    except sr.RequestError:
        logger.error("RequestError")

    return None


def clear_shell() -> None:
    """Clears any previous text in the shell"""
    os.system("cls")


def main() -> None:
    """Main function to interact with the user"""
    clear_shell()
    greeting()
    username()

    assname = "Jarvis 1 point 0"

    while True:
        query = speech_to_text()

        if query:
            parsed_text = query.lower()

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
                speak("Here you go to Youtube\n")
                webbrowser.open("youtube.com")

            elif "open google" in parsed_text:
                speak("Here you go to Google\n")
                webbrowser.open("google.com")

            elif "open stackoverflow" in parsed_text:
                speak("Here you go to Stack Over flow.Happy coding")
                webbrowser.open("stackoverflow.com")

            elif "the time" in parsed_text:
                strTime = datetime.datetime.now().strftime("% H:% M:% S")
                speak(f"Sir, the time is {strTime}")

            elif "how are you" in parsed_text:
                speak("I am fine, Thank you")
                speak("How are you, Sir")

            elif "fine" in parsed_text or "good" in parsed_text:
                speak("It's good to know that your fine")

            elif "change my name to" in parsed_text:
                parsed_text = parsed_text.replace("change my name to", "")
                assname = parsed_text

            elif "change name" in parsed_text:
                speak("What would you like to call me, Sir ")

                temp = speech_to_text()
                if temp is None:
                    logger.warning("No name was given")
                if temp:
                    assname = temp

                speak("Thanks for naming me")

            elif "what's your name" in parsed_text or "What is your name" in parsed_text:
                speak("My friends call me")
                speak(assname)
                print("My friends call me", assname)

            elif "exit" in parsed_text:
                speak("Thanks for giving me your time")
                exit()

            elif "who made you" in parsed_text or "who created you" in parsed_text:
                speak("I have been created by Gaurav.")

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

            elif "who i am" in parsed_text:
                speak("If you talk then definitely your human.")

            elif "why you came to world" in parsed_text:
                speak("Thanks to Gaurav. further It's a secret")

            elif "is love" in parsed_text:
                speak("It is 7th sense that destroy all other senses")

            elif "who are you" in parsed_text:
                speak("I am your virtual assistant created by Gaurav")

            elif "reason for you" in parsed_text:
                speak("I was created as a Minor project by Mister Gaurav ")

            elif "don't listen" in parsed_text or "stop listening" in parsed_text:
                speak("for how much time you want to stop jarvis from listening commands")

                temp = speech_to_text()
                a = int(temp if temp is not None else 60)
                time.sleep(a)
                print(a)

            elif "where is" in parsed_text:
                parsed_text = parsed_text.replace("where is", "")
                location = parsed_text
                speak("User asked to Locate")
                speak(location)
                webbrowser.open("https://www.google.nl / maps / place/" + location + "")

            elif "hibernate" in parsed_text or "sleep" in parsed_text:
                speak("Hibernating")
                subprocess.call("shutdown / h")

            elif "jarvis" in parsed_text:
                greeting()
                speak("Jarvis 1 point o in your service Mister")
                speak(assname)

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

            elif "Good Morning" in parsed_text:
                speak("A warm" + parsed_text)
                speak("How are you Mister")
                speak(assname)

            # most asked question from google Assistant
            elif "will you be my gf" in parsed_text or "will you be my bf" in parsed_text:
                speak("I'm not sure about, may be you should give me some time")

            elif "how are you" in parsed_text:
                speak("I'm fine, glad you me that")

            elif "i love you" in parsed_text:
                speak("It's hard to understand")


if __name__ == "__main__":
    main()
