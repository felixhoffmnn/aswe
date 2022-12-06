# ? Disable typing errors for pytest fixtures
# ? Disable private attribute access to test class methods
# pylint: disable=redefined-outer-name,protected-access

import json

import pytest
from pytest_mock import MockFixture
from requests.models import Response

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


@pytest.fixture
def import_paths() -> dict[str, str]:
    """Prepare import paths of functions which shall be mocked"""

    return {
        "http_request": "aswe.api.sport.football.http_request",
        "convert_league_name": "aswe.api.sport.football.convert_league_name",
        "get_teams": "aswe.api.sport.football.get_teams",
    }


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


# * test get_league_standings ----------------------------------------------------------
def test_get_league_standings(mocker: MockFixture, import_paths: dict[str, str]) -> None:
    """Test `aswe.api.sport.foodball.get_league_standings`

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    import_paths : dict[str, str]
        Fixture used for test setup
    """

    # * Mock valid response
    mock_valid_response_object = {
        "standings": [
            {
                "stage": "REGULAR_SEASON",
                "type": "TOTAL",
                "group": "None",
                "table": [
                    {
                        "position": 1,
                        "team": {
                            "name": "Arsenal FC",
                        },
                        "points": 37,
                    },
                    {
                        "position": 2,
                        "team": {
                            "name": "Manchester City FC",
                        },
                        "points": 32,
                    },
                ],
            }
        ],
    }
    valid_response = Response()
    valid_response._content = json.dumps(mock_valid_response_object).encode()
    mocker.patch(import_paths["http_request"], return_value=valid_response)
    mocker.patch(import_paths["convert_league_name"], return_value="PL")

    assert get_league_standings("test_name") == ["1. Arsenal FC - 37 points", "2. Manchester City FC - 32 points"]


def test_get_league_standings_invalid_response(mocker: MockFixture, import_paths: dict[str, str]) -> None:
    """Test `aswe.api.sport.football.get_league_standings` with invalid api responses

    Parameters
    ----------
    mocker : MockFixture
    import_paths : dict[str, str]
        Fixture used for test setup
    """

    # * Mock None league id
    mocker.patch(import_paths["convert_league_name"], return_value=None)

    assert get_league_standings("test_name") is None

    # * Mock None response
    mocker.patch(import_paths["convert_league_name"], return_value=1)
    mocker.patch(import_paths["http_request"], return_value=None)

    assert get_league_standings("league_name") is None


def test_get_matchday_matches(mocker: MockFixture, import_paths: dict[str, str]) -> None:
    """Test `aswe.api.sport.foodball.get_matchday_matches`

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    import_paths : dict[str, str]
        Fixture used for test setup
    """

    # * Mock valid response
    mock_valid_response_object = {
        "matches": [
            {
                "utcDate": "2022-12-03T15:00:00Z",
                "status": "FINISHED",
                "matchday": 4,
                "homeTeam": {
                    "name": "Netherlands",
                },
                "awayTeam": {
                    "name": "United States",
                },
                "score": {
                    "fullTime": {"home": 3, "away": 1},
                },
            }
        ]
    }
    valid_response = Response()
    valid_response._content = json.dumps(mock_valid_response_object).encode()
    mocker.patch(import_paths["http_request"], return_value=valid_response)
    mocker.patch(import_paths["convert_league_name"], return_value="test")

    assert get_matchday_matches("test_name", 4) == [
        "played on the 03.12.2022 at 16:00: Netherlands 3 to 1 United States"
    ]


def test_get_matchday_matches_invalid_response(mocker: MockFixture, import_paths: dict[str, str]) -> None:
    """Test `aswe.api.sport.football.get_matchday_matches` with invalid api responses

    Parameters
    ----------
    mocker : MockFixture
    import_paths : dict[str, str]
        Fixture used for test setup
    """

    # * Mock None league id
    mocker.patch(import_paths["convert_league_name"], return_value=None)

    assert get_matchday_matches("test_name", 3) is None

    # * Mock None response
    mocker.patch(import_paths["convert_league_name"], return_value=1)
    mocker.patch(import_paths["http_request"], return_value=None)

    assert get_matchday_matches("league_name", 3) is None


def test_get_ongoing_matches(mocker: MockFixture, import_paths: dict[str, str]) -> None:
    """Test `aswe.api.sport.foodball.get_ongoing_matches`

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    import_paths : dict[str, str]
        Fixture used for test setup
    """

    # * Mock valid response
    mock_valid_response_object = {
        "matches": [
            {
                "competition": {
                    "id": 2000,
                    "name": "FIFA World Cup",
                    "code": "WC",
                },
                "utcDate": "2022-12-03T15:00:00Z",
                "status": "IN_PLAY",
                "matchday": 4,
                "homeTeam": {
                    "name": "Netherlands",
                },
                "awayTeam": {
                    "name": "United States",
                },
                "score": {
                    "fullTime": {"home": 2, "away": 0},
                },
            }
        ]
    }
    valid_response = Response()
    valid_response._content = json.dumps(mock_valid_response_object).encode()
    mocker.patch(import_paths["http_request"], return_value=valid_response)
    mocker.patch(import_paths["convert_league_name"], return_value="WC")

    assert get_ongoing_matches("World Cup") == ["Netherlands 2 : 0 United States in FIFA World Cup"]


def test_get_ongoing_matches_invalid_response(mocker: MockFixture, import_paths: dict[str, str]) -> None:
    """Test `aswe.api.sport.football.get_ongoing_matches` with invalid api responses

    Parameters
    ----------
    mocker : MockFixture
    import_paths : dict[str, str]
        Fixture used for test setup
    """

    # * Mock None league id
    mocker.patch(import_paths["convert_league_name"], return_value=None)

    assert get_ongoing_matches("test_name") is None

    # * Mock None response
    mocker.patch(import_paths["convert_league_name"], return_value=1)
    mocker.patch(import_paths["http_request"], return_value=None)

    assert get_ongoing_matches("league_name") is None


def test_get_matches_today(mocker: MockFixture, import_paths: dict[str, str]) -> None:
    """Test `aswe.api.sport.foodball.get_matches_today`

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    import_paths : dict[str, str]
        Fixture used for test setup
    """

    # * Mock valid response
    mock_valid_response_object = {
        "matches": [
            {
                "competition": {
                    "id": 2000,
                    "name": "FIFA World Cup",
                    "code": "WC",
                },
                "utcDate": "2022-12-03T15:00:00Z",
                "status": "SCHEDULED",
                "matchday": 4,
                "homeTeam": {
                    "name": "Netherlands",
                },
                "awayTeam": {
                    "name": "United States",
                },
            }
        ]
    }
    valid_response = Response()
    valid_response._content = json.dumps(mock_valid_response_object).encode()
    mocker.patch(import_paths["http_request"], return_value=valid_response)
    mocker.patch(import_paths["convert_league_name"], return_value="WC")

    assert get_matches_today("World Cup") == ["playing at 16:00: Netherlands vs United States in FIFA World Cup"]


def test_get_matches_today_invalid_response(mocker: MockFixture, import_paths: dict[str, str]) -> None:
    """Test `aswe.api.sport.football.get_matches_today` with invalid api responses

    Parameters
    ----------
    mocker : MockFixture
    import_paths : dict[str, str]
        Fixture used for test setup
    """

    # * Mock None league id
    mocker.patch(import_paths["convert_league_name"], return_value=None)

    assert get_matches_today("test_name") is None

    # * Mock None response
    mocker.patch(import_paths["convert_league_name"], return_value=1)
    mocker.patch(import_paths["http_request"], return_value=None)

    assert get_matches_today("league_name") is None


def test_get_current_team_match(mocker: MockFixture, import_paths: dict[str, str]) -> None:
    """Test `aswe.api.sport.foodball.get_current_team_match`

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    import_paths : dict[str, str]
        Fixture used for test setup
    """

    # * Mock valid response
    mocker.patch(import_paths["get_teams"], return_value=["Netherlands", 1, "United States", 0, "Germany", 7])
    mocker.patch(import_paths["convert_league_name"], return_value="WC")
    mock_valid_response_object = {
        "matches": [
            {
                "competition": {
                    "id": 2000,
                    "name": "FIFA World Cup",
                    "code": "WC",
                },
                "utcDate": "2022-12-03T15:00:00Z",
                "status": "IN_PLAY",
                "matchday": 4,
                "homeTeam": {
                    "name": "Netherlands",
                },
                "awayTeam": {
                    "name": "United States",
                },
                "score": {
                    "fullTime": {"home": 2, "away": 0},
                },
            }
        ]
    }
    valid_response = Response()
    valid_response._content = json.dumps(mock_valid_response_object).encode()
    mocker.patch(import_paths["http_request"], return_value=valid_response)
    assert get_current_team_match("World Cup", "Netherlands") == ["Netherlands 2 : 0 United States in FIFA World Cup"]


def test_get_current_team_match_invalid_response(mocker: MockFixture, import_paths: dict[str, str]) -> None:
    """Test `aswe.api.sport.football.get_current_team_match` with invalid api responses

    Parameters
    ----------
    mocker : MockFixture
    import_paths : dict[str, str]
        Fixture used for test setup
    """

    # * Mock None league id
    mocker.patch(import_paths["get_teams"], return_value=None)

    assert get_current_team_match("World Cup", "Netherlands") is None

    mocker.patch(import_paths["get_teams"], return_value=["United States", 0, "Germany", 7])

    assert get_current_team_match("World Cup", "Netherlands") is None

    # * Mock None response
    mocker.patch(import_paths["get_teams"], return_value=["Netherlands", 1, "United States", 0, "Germany", 7])
    mocker.patch(import_paths["http_request"], return_value=None)

    assert get_current_team_match("World Cup", "Netherlands") is None


def test_get_upcoming_team_matches(mocker: MockFixture, import_paths: dict[str, str]) -> None:
    """Test `aswe.api.sport.foodball.get_upcoming_team_matches`

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    import_paths : dict[str, str]
        Fixture used for test setup
    """

    # * Mock valid response
    mocker.patch(import_paths["get_teams"], return_value=["Netherlands", 1, "United States", 0, "Germany", 7])
    mocker.patch(import_paths["convert_league_name"], return_value="WC")
    mock_valid_response_object = {
        "matches": [
            {
                "competition": {
                    "id": 2000,
                    "name": "FIFA World Cup",
                    "code": "WC",
                },
                "utcDate": "2022-12-03T15:00:00Z",
                "status": "SCHEDULED",
                "matchday": 4,
                "homeTeam": {
                    "name": "Netherlands",
                },
                "awayTeam": {
                    "name": "United States",
                },
            }
        ]
    }
    valid_response = Response()
    valid_response._content = json.dumps(mock_valid_response_object).encode()
    mocker.patch(import_paths["http_request"], return_value=valid_response)
    print(get_upcoming_team_matches("World Cup", "Netherlands"))
    assert get_upcoming_team_matches("World Cup", "Netherlands") == [
        "playing on the 03.12.2022 at 16:00: Netherlands vs United States"
    ]


def test_get_upcoming_team_matches_invalid_response(mocker: MockFixture, import_paths: dict[str, str]) -> None:
    """Test `aswe.api.sport.football.get_upcoming_team_match` with invalid api responses

    Parameters
    ----------
    mocker : MockFixture
    import_paths : dict[str, str]
        Fixture used for test setup
    """

    # * Mock None league id
    mocker.patch(import_paths["get_teams"], return_value=None)

    assert get_upcoming_team_matches("World Cup", "Netherlands") is None

    mocker.patch(import_paths["get_teams"], return_value=["United States", 0, "Germany", 7])

    assert get_upcoming_team_matches("World Cup", "Netherlands") is None

    # * Mock None response
    mocker.patch(import_paths["get_teams"], return_value=["Netherlands", 1, "United States", 0, "Germany", 7])
    mocker.patch(import_paths["http_request"], return_value=None)

    assert get_upcoming_team_matches("World Cup", "Netherlands") is None


def test_get_teams(mocker: MockFixture, import_paths: dict[str, str]) -> None:
    """Test `aswe.api.sport.foodball.get_teams`

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    import_paths : dict[str, str]
        Fixture used for test setup
    """

    # * Mock valid response
    mock_valid_response_object = {
        "teams": [
            {
                "id": 758,
                "name": "Uruguay",
            },
            {
                "id": 200,
                "name": "Netherlands",
            },
        ]
    }
    valid_response = Response()
    valid_response._content = json.dumps(mock_valid_response_object).encode()
    mocker.patch(import_paths["http_request"], return_value=valid_response)
    mocker.patch(import_paths["convert_league_name"], return_value="WC")

    assert get_teams("World Cup") == ["Uruguay", "758", "Netherlands", "200"]


def test_get_teams_invalid_response(mocker: MockFixture, import_paths: dict[str, str]) -> None:
    """Test `aswe.api.sport.football.get_teams` with invalid api responses

    Parameters
    ----------
    mocker : MockFixture
    import_paths : dict[str, str]
        Fixture used for test setup
    """

    # * Mock None league id
    mocker.patch(import_paths["convert_league_name"], return_value=None)

    assert get_teams("test_name") is None

    # * Mock None response
    mocker.patch(import_paths["convert_league_name"], return_value=1)
    mocker.patch(import_paths["http_request"], return_value=None)

    assert get_teams("league_name") is None
