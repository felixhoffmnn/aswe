import pytest

from aswe.api.sports.handball import (
    get_league_id,
    get_league_table,
    get_team_game_today,
    get_team_id,
)


# TODO fix test
@pytest.mark.xfail(reason="API limit reached")
def test_get_league_id() -> None:
    """Test `aswe.api.sports.handball.get_league_id`"""
    league_id = get_league_id("Bundesliga")
    assert league_id == 39


# TODO fix test
@pytest.mark.xfail(reason="API limit reached")
def test_get_league_table() -> None:
    """Test `aswe.api.sports.handball.get_league_table`"""
    standings = get_league_table("Bundesliga")
    assert len(standings) == 18


# TODO fix test
@pytest.mark.xfail(reason="API limit reached")
def test_get_team_id() -> None:
    """Test `aswe.api.sports.handball.get_team_id`"""
    team_id = get_team_id("Fuchse Berlin")
    assert team_id == 315


# TODO fix test
@pytest.mark.xfail(reason="API limit reached")
def test_get_team_game_today() -> None:
    """Test `aswe.api.sports.handball.get_team_game_today`"""
    game = get_team_game_today("Fuchse Berlin")
    assert isinstance(game, list)
