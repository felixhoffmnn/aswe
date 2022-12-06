from aswe.utils.text import calculate_similarity


def test_calulate_similarity() -> None:
    """Test the `calculate_similarity` function.

    This function is used to calculate the similarity between the parsed text
    and the options. The similarity indicates how similar the parsed text and
    the option are. The similarity is a value between 0 and 1.
    """
    assert calculate_similarity("Lorem", "Lorem") == 1.0
    assert calculate_similarity("Lorem", "Ipsum") < 0.5
    assert calculate_similarity("Lorem", ["Lorem", "Ipsum"]) == 1.0
    assert calculate_similarity("test", []) == 0.0
