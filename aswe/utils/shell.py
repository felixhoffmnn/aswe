import os
from sys import platform

from loguru import logger


def clear_shell() -> None:
    """Clears any previous text in the shell"""
    if platform in ["linux", "linux2", "darwin"]:
        os.system("clear")
    elif platform == "win32":
        os.system("cls")


def print_options(options: list[str | int]) -> None:
    """Prints a list of options to the shell

    Parameters
    ----------
    options : list[str  |  int]
        The list of options to print
    """
    print()

    if len(options) == 0:
        logger.warning("The options list is empty")
        return None

    for index, option in enumerate(options, start=1):
        print(f"{index}: {option}")

    return None


def get_int(options: list[str | int], start: int = 1) -> int | None:
    """Gets an integer from the user

    Parameters
    ----------
    options : list[int]
        The list of options to choose from
    start : int, optional
        The starting index of the options. This feature is useful if you also use
        the `print_options` function. _By default `1`._

    Returns
    -------
    int | None
        Returns the integer if it is in the list of options, otherwise returns None

    Raises
    ------
    ValueError
        If the input was invalid, but the error is caught within the function
    """
    print()

    if len(options) == 0:
        logger.warning("The options list is empty")
        return None

    choice = None
    while choice is None:
        try:
            choice = int(input("Enter a number: "))
            if choice < start or choice > len(options) + start - 1:
                raise ValueError
        except (ValueError, TypeError):
            logger.warning("Invalid input")
            choice = None

    # TODO: Python has a problem with do while loops
    return choice  # type: ignore
