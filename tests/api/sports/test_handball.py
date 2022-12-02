import pytest

from aswe.api.sport.handball import (
    get_league_id,
    get_league_table,
    get_team_game_today,
    get_team_id,
)
from aswe.utils.error import ApiLimitReached


@pytest.mark.xfail(raises=ApiLimitReached)
def test_get_league_id() -> None:
    """Test `aswe.api.sport.handball.get_league_id`"""
    league_id = get_league_id("Bundesliga")
    assert league_id == 39

    league_id = get_league_id("Testing")
    assert league_id is None


@pytest.mark.xfail(raises=ApiLimitReached)
def test_get_league_table() -> None:
    """Test `aswe.api.sport.handball.get_league_table`"""
    standings = get_league_table("Bundesliga")
    assert len(standings) == 18  # type: ignore

    standings = get_league_table("Testing")
    assert standings is None


@pytest.mark.xfail(raises=ApiLimitReached)
def test_get_team_id() -> None:
    """Test `aswe.api.sport.handball.get_team_id`"""
    team_id = get_team_id("Fuchse Berlin")
    assert team_id == 315

    team_id = get_team_id("Testing")
    assert team_id is None


@pytest.mark.xfail(raises=ApiLimitReached)
def test_get_team_game_today() -> None:
    """Test `aswe.api.sport.handball.get_team_game_today`"""
    game = get_team_game_today("Fuchse Berlin")
    assert isinstance(game, list)

    game = get_team_game_today("Testing")
    assert game is None

    game = get_team_game_today("Fuchse Berlin", "Testing")

    assert game is None
