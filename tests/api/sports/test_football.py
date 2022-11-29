from aswe.api.sports.football import (
    convert_league_name,
    get_current_team_match,
    get_league_standings,
    get_matchday_matches,
    get_matches_today,
    get_ongoing_matches,
    get_upcoming_team_matches,
)


def test_convert_league_name() -> None:
    """Test `aswe.api.sports.football.convert_league_name`"""
    name = convert_league_name("Bundesliga")

    assert isinstance(name, str)


def test_get_league_standings() -> None:
    """Test `aswe.api.sports.football.get_league_standings`"""
    standings = get_league_standings("PL")

    assert len(standings) == 20


def test_get_matchday_matches() -> None:
    """Test `aswe.api.sports.football.get_matchday_matches`"""
    matches = get_matchday_matches("FL1", 7)

    assert isinstance(matches, list)


def test_get_ongoing_matches() -> None:
    """Test `aswe.api.sports.football.get_matchday_matches`"""
    matches = get_ongoing_matches("BL1")

    assert isinstance(matches, list)


def test_get_matches_today() -> None:
    """Test `aswe.api.sports.football.get_matches_today`"""
    matches = get_matches_today("DED")

    assert isinstance(matches, list)


def test_get_current_team_match() -> None:
    """Test `aswe.api.sports.football.get_current_team_match`"""
    match = get_current_team_match("CL", "Frankfurt")

    assert isinstance(match, list)


def test_get_upcoming_team_matches() -> None:
    """Test `aswe.api.sports.football.get_upcoming_team_matches`"""
    matches = get_upcoming_team_matches("FL1", "PSG", 6)

    assert len(matches) == 6
