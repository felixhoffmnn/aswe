from aswe.api.sports.basketball import (
    get_nba_standings,
    get_team_game_today,
    get_team_id,
)


def test_get_nba_standings() -> None:
    """Test `aswe.api.sports.basketball.get_nba_standings`"""
    standings = get_nba_standings()

    assert len(standings) == 2 and len(standings[0]) == 15 and len(standings[1]) == 15


def test_get_team_game_today() -> None:
    """Test `aswe.api.sports.basketball.get_team_game_today`"""
    game = get_team_game_today("Boston Celtics")

    assert isinstance(game, list)


def test_get_team_id() -> None:
    """Test `aswe.api.sports.basketball.get_team_id`"""
    team_id = get_team_id("Denver Nuggets")

    assert isinstance(team_id, int)
