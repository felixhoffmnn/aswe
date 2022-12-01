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

    assert name == "Cl"
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


def test_get_league_standings() -> None:
    """Test `aswe.api.sports.football.get_league_standings`"""
    standings = get_league_standings("PL")

    assert len(standings) == 20

    standings = get_league_standings("Test")

    assert standings is None


def test_get_matchday_matches() -> None:
    """Test `aswe.api.sports.football.get_matchday_matches`"""
    matches = get_matchday_matches("FL1", 7)

    assert isinstance(matches, list)

    matches = get_matchday_matches("TS", 3)

    assert matches is None

    matches = get_matchday_matches("BL1", 700)

    assert matches is None


def test_get_ongoing_matches() -> None:
    """Test `aswe.api.sports.football.get_matchday_matches`"""
    matches = get_ongoing_matches("BL1")

    assert isinstance(matches, list)

    matches = get_ongoing_matches("TS")

    assert matches is None

    # only works till next European Championship 2024
    matches = get_ongoing_matches("EC")

    assert matches == ["No matches are currently being played."]


def test_get_matches_today() -> None:
    """Test `aswe.api.sports.football.get_matches_today`"""
    matches = get_matches_today("DED")

    assert isinstance(matches, list)

    matches = get_matches_today("TS")

    assert matches is None


def test_get_current_team_match() -> None:
    """Test `aswe.api.sports.football.get_current_team_match`"""
    match = get_current_team_match("CL", "Frankfurt")

    assert isinstance(match, list)

    match = get_current_team_match("CL", "Test")

    assert match is None

    match = get_current_team_match("TS", "Frankfurt")

    assert match is None


def test_get_upcoming_team_matches() -> None:
    """Test `aswe.api.sports.football.get_upcoming_team_matches`"""
    matches = get_upcoming_team_matches("FL1", "PSG", 6)

    assert len(matches) == 6

    match = get_current_team_match("CL", "Test")

    assert match is None

    match = get_current_team_match("TS", "Frankfurt")

    assert match is None
