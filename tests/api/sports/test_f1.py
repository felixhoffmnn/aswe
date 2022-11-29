from aswe.api.sports.f1 import (
    get_results_by_round,
    get_results_last_round,
    get_results_next_round,
)


def test_get_results_by_round() -> None:
    """Test `aswe.api.sports.f1.get_results_by_round`"""
    results = get_results_by_round(2017, "19")

    assert len(results) == 20


def test_get_results_last_round() -> None:
    """Test `aswe.api.sports.f1.get_results_last_round`"""
    results = get_results_last_round()

    assert len(results) == 20 or len(results) == 0


def test_get_results_next_round() -> None:
    """Test `aswe.api.sports.f1.get_results_next_round`"""
    results = get_results_next_round()

    assert len(results) == 20 or len(results) == 0
