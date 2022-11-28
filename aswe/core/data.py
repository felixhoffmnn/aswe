from dataclasses import dataclass


@dataclass
class BestMatch:
    """Dataclass to store the best match for a given user input.

    Parameters
    ----------
    use_case : str
        The name of the use case.
    function_key : str
        The key of the function which should be called.
    similarity : float
        The similarity between the user input and the best match.
    parsed_text : str
        The parsed text from the user input.
    """

    use_case: str
    """The name of the use case."""

    function_key: str
    """The key of the function which should be called."""

    similarity: float
    """The similarity between the user input and the best match."""

    parsed_text: str
    """The parsed text from the user input."""


@dataclass
class User:
    """Dataclass supposed to store the user data

    * TODO: Add more attributes and evaluate the existing ones
    * TODO: User has a car?

    Parameters
    ----------
    name : str | None, optional
        The name of the user.
    age : int | None, optional
        The age of the user. _By default `None`_.
    street : str | None, optional
        The street of the user. _By default `None`_.
    city : str | None, optional
        The city of the user. _By default `None`_.
    zip_code : int | None, optional
        The zip code of the user. _By default `None`_.
    country : str | None, optional
        The country of the user. _By default `None`_.
    """

    name: str | None
    """The name of the user."""

    age: int | None = None
    """The age of the user. _By default `None`_."""

    street: str | None = None
    """The street of the user. _By default `None`_."""

    city: str | None = None
    """The city of the user. _By default `None`_."""

    zip_code: int | None = None
    """The zip code of the user. _By default `None`_."""

    country: str | None = None
    """The country of the user. _By default `None`_."""
