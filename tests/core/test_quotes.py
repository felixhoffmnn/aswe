import json
from itertools import chain
from pathlib import Path


def test_unique_values() -> None:
    """Test if all values in `quotes.json` are unique

    Raises
    ------
    ValueError
        If a value is not unique.
    """
    with open(Path("data/use_case/quotes.json"), encoding="utf-8") as file:
        quotes = json.load(file)
    assert quotes is not None, "Quotes are None"

    list_of_triggers = list(chain.from_iterable([list(chain.from_iterable(e.values())) for e in quotes.values()]))
    assert len(list_of_triggers) == len(set(list_of_triggers)), "Not all values are unique"
