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
    with open(Path("data/quotes.json"), encoding="utf-8") as file:
        quotes = json.load(file)
    assert quotes is not None, "Quotes are None"

    temp_list = []
    for element in quotes.values():
        for use_case in element.values():
            temp_list.append(use_case)
            assert isinstance(use_case, list), "Use case is not a list"

    list_of_triggers = list(chain.from_iterable(temp_list))
    assert len(list_of_triggers) == len(set(list_of_triggers)), "Not all values are unique"
