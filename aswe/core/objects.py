from dataclasses import dataclass
from datetime import datetime


@dataclass
class LogProactivity:
    """A class to keep track of the last time proactivity was triggered

    Attributes
    ----------
    last_event_check : datetime
        The last time the event use case was triggered
    last_morning_briefing_check : datetime
        The last time the morning briefing was triggered
    last_sport_check : datetime
        The last time the sport use case was triggered
    last_transportation_check : datetime
        The last time the transportation use case was triggered
    """

    last_event_check: datetime = datetime.now()
    last_morning_briefing_check: datetime = datetime.now()
    last_sport_check: datetime = datetime.now()
    last_transportation_check: datetime = datetime.now()


@dataclass
class BestMatch:
    """Dataclass to store the best match for a given user input.

    Attributes
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
    function_key: str
    similarity: float
    parsed_text: str


@dataclass
class Address:
    """Dataclass to store the address of a user.

    Attributes
    ----------
    street : str
        The street of the user.
    city : str
        The city of the user.
    zip_code : int
        The zip code of the user.
    country : str
        The country of the user.
    vvs_id : str
        The VVS ID of the user.
    """

    street: str
    city: str
    zip_code: int
    country: str
    vvs_id: str


@dataclass
class Possessions:
    """Dataclass to store the possessions of a user.

    Attributes
    ----------
    bike : bool
        Does the user own a bike?
    car : bool
        Does the user own a car?
    """

    bike: bool
    car: bool


@dataclass
class Favorites:
    """Dataclass to store the favorites of a user.

    For example the favorite stocks, sports teams, etc.

    Parameters
    ----------
    stocks : list[str]
        The favorite stocks of the user.
    league : str
        The favorite league of the user.
    team : str
        The favorite team of the user.
    news_keywords : list[str]
        The favorite news keywords of the user.
    wakeup_time : datetime
        The wakeup time of the user.
    """

    stocks: list[dict[str, str]]
    league: str
    team: str
    news_keywords: list[str]
    wakeup_time: datetime


@dataclass
class User:
    """Dataclass supposed to store the user data

    * TODO: Add more attributes and evaluate the existing ones

    Attributes
    ----------
    name : str
        The name of the user.
    age : int
        The age of the user.
    address : Address
        The address of the user.
    favorites : Favorites
    """

    name: str
    age: int
    address: Address
    possessions: Possessions
    favorites: Favorites
