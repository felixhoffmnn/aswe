import pytest

from aswe.api.sport.football import (
    convert_league_name,
    get_current_team_match,
    get_league_standings,
    get_matchday_matches,
    get_matches_today,
    get_ongoing_matches,
    get_teams,
    get_upcoming_team_matches,
)
from aswe.utils.error import TooManyRequests


def test_convert_league_name() -> None:
    """Test `aswe.api.sport.football.convert_league_name`"""
    name = convert_league_name("Testing")

    assert name is None
    name = convert_league_name("Premier League")

    assert name == "PL"
    name = convert_league_name("Spanish League")

    assert name == "PD"
    name = convert_league_name("Italian League")

    assert name == "SA"
    name = convert_league_name("German League")

    assert name == "BL1"
    name = convert_league_name("French League")

    assert name == "FL1"
    name = convert_league_name("World Cup")

    assert name == "WC"
    name = convert_league_name("UEFA Champions League")

    assert name == "CL"
    name = convert_league_name("Dutch League")

    assert name == "DED"
    name = convert_league_name("Brazilian League")

    assert name == "BSA"
    name = convert_league_name("English League 2")

    assert name == "ELC"
    name = convert_league_name("Primeira Liga")

    assert name == "PPL"
    name = convert_league_name("European Championship")

    assert name == "EC"


@pytest.mark.xfail(raises=TooManyRequests)
def test_get_league_standings() -> None:
    """Test `aswe.api.sport.football.get_league_standings`"""
    standings = get_league_standings("Premier League")

    assert isinstance(standings, list) and len(standings) == 20

    standings = get_league_standings("Test")

    assert standings is None


@pytest.mark.xfail(raises=TooManyRequests)
def test_get_matchday_matches() -> None:
    """Test `aswe.api.sport.football.get_matchday_matches`"""
    matches = get_matchday_matches("Bundesliga", 7)

    assert isinstance(matches, list)

    matches = get_matchday_matches("TS", 3)

    assert matches is None

    matches = get_matchday_matches("Bundesliga", 700)

    assert matches is None


@pytest.mark.xfail(raises=TooManyRequests)
def test_get_ongoing_matches() -> None:
    """Test `aswe.api.sport.football.get_matchday_matches`"""
    matches = get_ongoing_matches("Primera Division")

    assert isinstance(matches, list)

    matches = get_ongoing_matches("TS")

    assert matches is None

    # only works till next European Championship 2024
    matches = get_ongoing_matches("European Championship")

    assert matches == ["No matches are currently being played."]


@pytest.mark.xfail(raises=TooManyRequests)
def test_get_matches_today() -> None:
    """Test `aswe.api.sport.football.get_matches_today`"""
    matches = get_matches_today("Bundesliga")

    assert isinstance(matches, list)

    matches = get_matches_today("TS")

    assert matches is None


@pytest.mark.xfail(raises=TooManyRequests)
def test_get_current_team_match() -> None:
    """Test `aswe.api.sport.football.get_current_team_match`"""
    match = get_current_team_match("Champions League", "Frankfurt")

    assert isinstance(match, list)

    match = get_current_team_match("Bundesliga", "Test")

    assert match is None

    match = get_current_team_match("TS", "Frankfurt")

    assert match is None


@pytest.mark.xfail(raises=TooManyRequests)
def test_get_upcoming_team_matches() -> None:
    """Test `aswe.api.sport.football.get_upcoming_team_matches`"""
    matches = get_upcoming_team_matches("Ligue 1", "PSG", 6)

    assert isinstance(matches, list) and len(matches) == 6

    match = get_current_team_match("Champions Ligue", "Test")

    assert match is None

    match = get_current_team_match("TS", "Frankfurt")

    assert match is None


@pytest.mark.xfail(raises=TooManyRequests)
def test_get_teams() -> None:
    """Test `aswe.api.sport.football.get_teams`"""
    teams = get_teams("Premier League")

    assert isinstance(teams, list) and len(teams) == 20

    teams = get_teams("TS")

    assert teams is None
