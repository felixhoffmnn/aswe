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
    function_key: str
    similarity: float
    parsed_text: str


@dataclass
class Address:
    """Dataclass to store the address of a user.

    Parameters
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

    Parameters
    ----------
    bike : bool
        Does the user own a bike?
    car : bool
        Does the user own a car?
    """

    bike: bool
    car: bool


@dataclass
class User:
    """Dataclass supposed to store the user data

    * TODO: Add more attributes and evaluate the existing ones
    * TODO: User has a car?

    Parameters
    ----------
    name : str
        The name of the user.
    age : int
        The age of the user.
    address : Address
        The address of the user.
    favorite_stocks : list[str]
        The favorite stocks of the user.
    """

    name: str
    age: int
    address: Address
    possessions: Possessions
    favorite_stocks: list[str]
