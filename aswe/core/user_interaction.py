import re
import time
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import pyttsx3
import speech_recognition as sr
from loguru import logger

from aswe.utils.shell import clear_shell, get_int, print_options
from aswe.utils.text import calculate_similarity


class SpeechToText:
    """Class to convert speech to text."""

    def __init__(self, get_mic: bool) -> None:
        """Initializes the speech to text class.

        * TODO: Think about a better way to handle the case that the `microphone_index` is not required
        * TODO: Add Attributes section
        * TODO: Add test method

        Parameters
        ----------
        get_mic : bool
            If the speech to text class should first get the microphone index.
        """
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 800

        if get_mic:
            clear_shell()

            print("At first, please select the microphone you want to use.\n")
            time.sleep(1)

            list_of_microphones = sr.Microphone.list_microphone_names()
            print_options(list_of_microphones)
            choice = get_int(list_of_microphones, start=1)
            self.microphone_index = choice

        if not get_mic:
            self.microphone_index = None

    def check_if_yes(self) -> bool:
        """First gets the user input and then checks if the user said yes.

        Returns
        -------
        bool
            Boolean if the user said yes.
        """
        logger.debug("Checking if the user says yes...")
        parsed_text = self.convert_speech()

        if parsed_text is None:
            logger.warning("No text could be parsed. Maybe an error occurred?")
            return False

        return calculate_similarity(parsed_text, ["yes", "yeah", "yep", "sure", "ok", "okay", "ja"]) == 1

    def convert_audio_file(self, audio_file: str | Path) -> str | None:
        """Converts an audio file to text.

        * TODO: For now this function is only for testing purposes

        Parameters
        ----------
        audio_file : str | Path
            The path to the audio file which should be converted.

        Returns
        -------
        str | None
            The parsed text or `None` if the parsing failed.
        """
        try:
            with sr.AudioFile(str(audio_file)) as source:
                audio = self.recognizer.record(source)
                parsed_text = self.recognizer.recognize_google(audio, language="en-US")

            if isinstance(parsed_text, str):
                return parsed_text

            logger.warning("The speech recognition did not return a string.")
        except sr.UnknownValueError:
            logger.warning(
                "The speech recognition was not able to understand anything. Did you say something? If so, please try again."
            )
        except sr.RequestError:
            logger.error(
                "The speech recognition operation failed, maybe due to a invalid API key or no internet connection."
            )

        return None

    def convert_speech(self, line_above: bool = False) -> str | None:
        """First records an audio file an then pareses it to text.

        When the function does not detect any speech for `60` seconds it will timeout and return `None`.

        * TODO: Check `adjust_for_ambient_noise`
        * TODO: Add function to cancel the request without quitting the program

        Parameters
        ----------
        line_above : bool, optional
            If a new line should be printed before the user input. _By default `False`._

        Returns
        -------
        str | None
            The parsed text or None if no text could be parsed.
        """
        if line_above:
            print()

        audio: sr.AudioData | None = None

        with sr.Microphone(self.microphone_index) as source:
            print("Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=60)
            except sr.WaitTimeoutError:
                logger.warning("The speech recognition timed out.")

        if audio is not None:
            try:
                print("Recognizing...")
                with redirect_stdout(StringIO()) as output:
                    parsed_text = self.recognizer.recognize_google(audio, language="en-US")
                    logger.debug(output.getvalue().replace("\n", " ").replace(r"/  +/g", " "))

                if isinstance(parsed_text, str):
                    print(f"User: {parsed_text}")
                    return parsed_text

                logger.warning("The speech recognition did not return a string.")
            except sr.UnknownValueError:
                logger.warning(
                    "The speech recognition was not able to understand anything. Did you say something? If so, please try again."
                )
                return None
            except sr.RequestError:
                logger.error(
                    "The speech recognition operation failed, maybe due to a invalid API key or no internet connection."
                )
                return None

        return None


class TextToSpeech:
    """Class to convert text to speech."""

    def __init__(self) -> None:
        """Initializes the text to speech class.

        * TODO: Add Attributes section
        * TODO: Add test method
        """
        self.engine: pyttsx3.Engine = pyttsx3.init()
        self.engine.setProperty("rate", 175)
        self.engine.setProperty("voice", "english")

    def optimize_text(
        self,
        text: str,
        optimize_time: bool,
        optimize_numbers: bool,
    ) -> str:
        """Optimizes text with time indications (in HH:MM format) for speech.

        Parameters
        ----------
        text : str
            The text which should be optimized.
        optimize_time : bool, optional
            If the time should be optimized for speech. Will replace `22:00` with `22 o'clock`
            and `22:30` with `22 30`. _By default `True`._
        optimize_numbers : bool, optional
            If the numbers should be optimized for speech. Will replace `22.` with `22 .`. _By default `True`._

        Returns
        -------
        str
            The optimized text.
        """
        if optimize_numbers:
            text = re.sub(r"(\d+)\.", r"\1 .", text)

        if optimize_time:
            text = text.replace(":00", " o'clock")
            text = re.sub(r"0(\d{1}) o'clock", r"\1 o'clock", text)
            text = re.sub(r"0(\d{1}):(\d{2})", r"\1 \2", text)
            text = re.sub(r"(\d{2}):(\d{2})", r"\1 \2", text)

        return text

    def convert_text(
        self,
        text: str,
        optimize_time: bool = True,
        optimize_numbers: bool = True,
        line_above: bool = False,
    ) -> None:
        """Converts text to speech

        Parameters
        ----------
        text : str
            The Text which should be converted to speech.
        optimize_time : bool, optional
            If the time should be optimized for speech. Will replace `22:00` with `22 o'clock`
            and `22:30` with `22 30`. _By default `True`._
        optimize_numbers : bool, optional
            If the numbers should be optimized for speech. Will replace `22.` with `22 .`. _By default `True`._
        line_above : bool, optional
            If a new line should be printed before the bot input. _By default `False`_.
        """
        if line_above:
            print()

        logger.debug(f"Converting text to speech: {text.strip()}")

        print(f"Bot: {text.strip()}")

        if optimize_time or optimize_numbers:
            text = self.optimize_text(text, optimize_time, optimize_numbers)
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except RuntimeError:
            logger.error("The text to speech engine is already in use.")
