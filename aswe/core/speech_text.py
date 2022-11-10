import time

import pyttsx3
import speech_recognition as sr
from loguru import logger


class SpeechToText:
    """Class to convert speech to text."""

    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()

        print("At first, please select the microphone you want to use.\n")
        time.sleep(1)
        list_of_microphones = sr.Microphone.list_microphone_names()
        for index, name in enumerate(list_of_microphones):
            print(f"Microphone with name <<{name}>> found for `Microphone(device_index={index})`")
        print("\nPlease enter the index of the microphone you want to use.")
        self.microphone_index = int(input())

    def get_speech(self) -> str | None:
        """First records an audio file an then pareses it to text.

        * TODO: Check `adjust_for_ambient_noise`

        Returns
        -------
        str | None
            The parsed text or None if no text could be parsed.
        """
        with sr.Microphone(self.microphone_index) as source:
            # self.recognizer.adjust_for_ambient_noise(source, duration=1)
            self.recognizer.energy_threshold = 2500
            self.recognizer.pause_threshold = 1

            print("Listening...")
            audio = self.recognizer.listen(source)

        try:
            print("Recognizing...")
            parsed_text = self.recognizer.recognize_google(audio, language="en-US")

            if isinstance(parsed_text, str):
                print(f"User: {parsed_text}")
                return parsed_text
        except sr.UnknownValueError:
            logger.warning(
                "The speech recognition was not able to understand anything. Did you say something? If so, please try again."
            )
        except sr.RequestError:
            logger.error(
                "The speech recognition operation failed, maybe due to a invalid API key or no internet connection."
            )
        except sr.WaitTimeoutError:
            logger.warning("While listening, the wait timeout was reached.")

        return None


class TextToSpeech:
    """Class to convert text to speech."""

    def __init__(self) -> None:
        self.engine = pyttsx3.init()
        self.engine.setProperty("voice", "english")

    def convert_text(self, text: str) -> None:
        """Converts text to speech

        Parameters
        ----------
        audio : str
            The Text which should be converted to speech.
        """
        logger.debug(f"Converting text to speech: {text.strip()}")

        print(f"HiBuddy: {text.strip()}")
        self.engine.say(text)
        self.engine.runAndWait()
