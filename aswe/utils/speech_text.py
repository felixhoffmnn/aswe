import pyttsx3
import speech_recognition as sr
from loguru import logger


def speech_to_text(recognizer: sr.Recognizer) -> str | None:
    """First records an audio file an then pareses it to text

    Returns
    -------
    str | None
        The parsed text or None if no text could be parsed
    """

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        parsed_text = recognizer.recognize_google(audio, language="en-US")
        print(f"\nUser said: {parsed_text}\n")

        if isinstance(parsed_text, str):
            return parsed_text
    except sr.UnknownValueError:
        logger.error("UnknownValueError")
    except sr.RequestError:
        logger.error("RequestError")

    return None


def text_to_speech(text: str, engine: pyttsx3.Engine) -> None:
    """Converts text to speech

    Parameters
    ----------
    audio : str
        The Text which should be converted to speech
    """
    logger.debug(f"Converting text to speech: {text}")
    engine.setProperty("voice", "english")

    engine.say(text)
    engine.runAndWait()
