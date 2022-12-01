import time
from pathlib import Path

import pyttsx3
import speech_recognition as sr
from loguru import logger

from aswe.utils.shell import clear_shell


class SpeechToText:
    """Class to convert speech to text."""

    def __init__(self, get_mic_index: bool, is_test: bool) -> None:
        """Initializes the speech to text class.

        * TODO: Think about a better way to handle the case that the `microphone_index` is not required
        * TODO: Add Attributes section
        * TODO: Add test method

        Parameters
        ----------
        get_mic_index : bool
            If the speech to text class should first get the microphone index.
        is_test : bool, optional
            Boolean if the agent is used for testing. _By default `False`_.
        """
        self.is_test = is_test
        self.recognizer = sr.Recognizer()

        if get_mic_index:
            clear_shell()

            print("At first, please select the microphone you want to use.\n")
            time.sleep(1)
            list_of_microphones = sr.Microphone.list_microphone_names()
            for index, name in enumerate(list_of_microphones):
                print(f"Microphone with name <<{name}>> found for `Microphone(device_index={index})`")
            print("\nPlease enter the index of the microphone you want to use.")
        self.microphone_index = int(input("Microphone index: ")) if get_mic_index else None

    def convert_audio_file(self, audio_file: str | Path) -> str | None:
        """Converts an audio file to text.

        * TODO: For now this function is only for testing purposes

        Parameters
        ----------
        audio_file : str | Path
            The path to the audio file which should be converted.
        """
        try:
            with sr.AudioFile(str(audio_file)) as source:
                audio = self.recognizer.record(source)
                parsed_text = self.recognizer.recognize_google(audio, language="en-US")

            if isinstance(parsed_text, str):
                return parsed_text
        except sr.UnknownValueError:
            logger.warning(
                "The speech recognition was not able to understand anything. Did you say something? If so, please try again."
            )
        except sr.RequestError:
            logger.error(
                "The speech recognition operation failed, maybe due to a invalid API key or no internet connection."
            )

        return None

    def convert_speech(self) -> str | None:
        """First records an audio file an then pareses it to text.

        When the function does not detect any speech for `60` seconds it will timeout and return `None`.

        * TODO: Check `adjust_for_ambient_noise`

        Returns
        -------
        str | None
            The parsed text or None if no text could be parsed.
        """
        audio: sr.AudioData | None = None

        with sr.Microphone(self.microphone_index) as source:
            # self.recognizer.adjust_for_ambient_noise(source, duration=1)
            self.recognizer.energy_threshold = 2500
            self.recognizer.pause_threshold = 1

            print("Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=60)
            except sr.WaitTimeoutError:
                logger.warning("The speech recognition timed out.")

        if audio is not None:
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

        return None


class TextToSpeech:
    """Class to convert text to speech."""

    def __init__(self, is_test: bool) -> None:
        """Initializes the text to speech class.

        * TODO: Add Attributes section
        * TODO: Add test method
        * TODO: Replace with `gTTS`

        Parameters
        ----------
        is_test : bool, optional
            Boolean if the agent is used for testing. _By default `False`_.
        """
        self.is_test = is_test

        self.engine: pyttsx3.Engine = pyttsx3.init()
        self.engine.setProperty("rate", 175)
        self.engine.setProperty("voice", "english")

    def convert_text(self, text: str) -> None:
        """Converts text to speech

        Parameters
        ----------
        text : str
            The Text which should be converted to speech.
        """
        logger.debug(f"Converting text to speech: {text.strip()}")

        print(f"Bot: {text.strip()}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except RuntimeError:
            logger.error("The text to speech engine is already in use.")
