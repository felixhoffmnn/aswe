from datetime import datetime

from loguru import logger

# def uc_morning_briefing(parsed_text: str, quotes: dict[str, list[str]]) -> None:
#     """Lorem Ipsum

#     * TODO: Implement
#     """


# def uc_events(parsed_text: str, quotes: dict[str, list[str]]) -> None:
#     """Lorem Ipsum

#     * TODO: Implement
#     """


# def uc_transportation(parsed_text: str, quotes: dict[str, list[str]]) -> None:
#     """Lorem Ipsum

#     * TODO: Implement
#     """


def uc_general(parsed_text: str, quotes: dict[str, list[str]]) -> str | None:
    """UseCase for general questions

    Parameters
    ----------
    parsed_text : str
        The voice input of the user parsed to lower case string
    quotes : dict[str, list[str]]
        The dictionary of quotes regarding the general use case

    Returns
    -------
    str | None
        The response as a string or None if the request is not implemented
    """
    if parsed_text in quotes["time"]:
        logger.debug(f"uc_general({parsed_text}, {quotes}).time")
        current_time = datetime.now().strftime("%H:%M")
        return f"The current time is {current_time}"

    return None
