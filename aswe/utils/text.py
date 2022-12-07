from difflib import SequenceMatcher


def calculate_similarity(parsed_text: str, options: list[str] | str) -> float:
    """Calculates the similarity between the parsed text and all options.
    Returns the highest similarity.

    Parameters
    ----------
    parsed_text : str
        The parsed text from the user input.
    options : list[str] | str
        The options which should be compared with the parsed text.

    Returns
    -------
    float
        If a list of options is given, the highest similarity is returned.
        Else the similarity of the parsed text and the option is returned.
    """
    if isinstance(options, str):
        options = [options]

    if len(options) == 0:
        return 0.0

    return max(SequenceMatcher(None, parsed_text, option).quick_ratio() for option in options)
