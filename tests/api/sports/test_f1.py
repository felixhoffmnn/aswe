from aswe.api.sport.f1 import (
    get_results_by_round,
    get_results_last_round,
    get_results_next_round,
)


def test_get_results_by_round() -> None:
    """Test `aswe.api.sport.f1.get_results_by_round`"""
    results = get_results_by_round(2017, 19)

    if results is not None:
        assert len(results) == 20

    results = get_results_by_round(2030, 20)

    assert results is None

    results = get_results_by_round(2023, 1)

    assert results is None


def test_get_results_last_round() -> None:
    """Test `aswe.api.sport.f1.get_results_last_round`"""
    results = get_results_last_round()
    if results is not None:
        assert len(results) == 20 or len(results) == 0


def test_get_results_next_round() -> None:
    """Test `aswe.api.sport.f1.get_results_next_round`"""
    results = get_results_next_round()
    if results is not None:
        assert len(results) == 20 or len(results) == 0
