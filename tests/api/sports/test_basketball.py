import pytest

from aswe.api.sport.basketball import (
    get_nba_standings,
    get_nba_teams,
    get_team_game_today,
    get_team_id,
)
from aswe.utils.error import ApiLimitReached


@pytest.mark.xfail(raises=ApiLimitReached)
def test_get_nba_standings() -> None:
    """Test `aswe.api.sport.basketball.get_nba_standings`"""
    standings = get_nba_standings()

    assert isinstance(standings, list) and len(standings) == 2 and len(standings[0]) == 15 and len(standings[1]) == 15


@pytest.mark.xfail(raises=ApiLimitReached)
def test_get_nba_teams() -> None:
    """Test `aswe.api.sport.basketball.get_nba_teams`"""
    teams = get_nba_teams()

    assert isinstance(teams, list) and len(teams) == 60


@pytest.mark.xfail(raises=ApiLimitReached)
def test_get_team_game_today() -> None:
    """Test `aswe.api.sport.basketball.get_team_game_today`"""
    game = get_team_game_today("Boston Celtics")

    assert isinstance(game, list)

    game = get_team_game_today("Testing")

    assert game is None


@pytest.mark.xfail(raises=ApiLimitReached)
def test_get_team_id() -> None:
    """Test `aswe.api.sport.basketball.get_team_id`"""
    team_id = get_team_id("Denver Nuggets")

    assert isinstance(team_id, int)

    team_id = get_team_id("Testing")

    assert team_id is None  # , "test"
