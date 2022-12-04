# ? Disable typing errors for pytest fixtures
# ? Disable private attribute access to test class methods
# pylint: disable=redefined-outer-name,protected-access

import json
from typing import Any

import pytest
from pytest_mock import MockFixture
from requests.models import Response

from aswe.api.sport.handball import (
    get_league_id,
    get_league_table,
    get_team_game_today,
    get_team_id,
)
from aswe.utils.error import ApiLimitReached


@pytest.fixture
def import_paths() -> dict[str, str]:
    """Prepare import paths of functions which shall be mocked"""

    import_paths = {
        "http_request": "aswe.api.sport.handball.http_request",
        "validate_api": "aswe.api.sport.handball.validate_api",
        "get_league_id": "aswe.api.sport.handball.get_league_id",
        "get_team_id": "aswe.api.sport.handball.get_team_id",
    }

    return import_paths


# * get_league_id -------------------------------------------------------------
def test_get_league_id(mocker: MockFixture, import_paths: dict[str, str]) -> None:
    """Test `aswe.api.sport.handball.get_league_id`

    Parameters
    ----------
    mocker : MockFixture
    import_paths : dict[str, str]
        Fixture used for test setup
    """

    # * Mock valid response
    mock_valid_response_object = {"response": [{"id": "1", "name": "test_name"}]}
    valid_response = Response()
    valid_response._content = json.dumps(mock_valid_response_object).encode()
    mocker.patch(import_paths["http_request"], return_value=valid_response)
    mocker.patch(import_paths["validate_api"], return_value=False)

    assert get_league_id("test_name") == 1


def test_get_league_id_invalid_response(mocker: MockFixture, import_paths: dict[str, str]) -> None:
    """Test `aswe.api.sport.handball.get_league_id` with invalid api responses

    Parameters
    ----------
    mocker : MockFixture
    import_paths : dict[str, str]
        Fixture used for test setup
    """

    # * Mock None response
    mocker.patch(import_paths["http_request"], return_value=None)

    assert get_league_id("test_name") is None

    # * Mock empty response
    mock_empty_response_object: dict[str, list[Any]] = {"response": []}
    empty_response = Response()
    empty_response._content = json.dumps(mock_empty_response_object).encode()
    mocker.patch(import_paths["http_request"], return_value=empty_response)

    assert get_league_id("test_name") is None


def test_get_league_id_api_limit(mocker: MockFixture, import_paths: dict[str, str]) -> None:
    """Test `aswe.api.sport.handball.get_league_id` when ApiLimits is reached

    Parameters
    ----------
    mocker : MockFixture
    import_paths : dict[str, str]
        Fixture used for test setup
    """

    mock_empty_response_object: dict[str, list[Any]] = {"response": []}
    empty_response = Response()
    empty_response._content = json.dumps(mock_empty_response_object).encode()

    # * Mock ApiLimitReached
    mocker.patch(import_paths["http_request"], return_value=empty_response)
    mocker.patch(import_paths["validate_api"], return_value=True)

    with pytest.raises(ApiLimitReached, match="You have reached the handball API request limit for the day"):
        get_league_id("test_name")


# * ---------------------------------------------------------------------------

# * get_league_table ----------------------------------------------------------
def test_get_league_table(mocker: MockFixture, import_paths: dict[str, str]) -> None:
    """Test `aswe.api.sport.handball.get_league_table`

    Parameters
    ----------
    mocker : MockFixture
        _description_
    import_paths : dict[str, str]
        Fixture used for test setup
    """

    # * Mock valid response
    mock_valid_response_object = {
        "response": [[{"position": "test_position", "team": {"name": "test_team_name"}, "points": "test_points"}]]
    }
    valid_response = Response()
    valid_response._content = json.dumps(mock_valid_response_object).encode()
    mocker.patch(import_paths["http_request"], return_value=valid_response)
    mocker.patch(import_paths["get_league_id"], return_value=1)
    mocker.patch(import_paths["validate_api"], return_value=False)

    assert get_league_table("test_name") == ["test_position test_team_name test_points"]


def test_get_league_table_invalid_response(mocker: MockFixture, import_paths: dict[str, str]) -> None:
    """Test `aswe.api.sport.handball.get_league_table` with invalid api responses

    Parameters
    ----------
    mocker : MockFixture
    import_paths : dict[str, str]
        Fixture used for test setup
    """

    # * Mock None league id
    mocker.patch(import_paths["get_league_id"], return_value=None)

    assert get_league_table("test_name") is None

    # * Mock None response
    mocker.patch(import_paths["get_league_id"], return_value=1)
    mocker.patch(import_paths["http_request"], return_value=None)

    assert get_league_table("league_name") is None

    # * Mock empty response
    mock_empty_response_object: dict[str, list[Any]] = {"response": [[]]}
    empty_response = Response()
    empty_response._content = json.dumps(mock_empty_response_object).encode()
    mocker.patch(import_paths["http_request"], return_value=empty_response)

    assert get_league_table("test_name") == []


def test_get_league_table_api_limit(mocker: MockFixture, import_paths: dict[str, str]) -> None:
    """Test `aswe.api.sport.handball.get_league_id` when ApiLimits is reached

    Parameters
    ----------
    mocker : MockFixture
        _description_
    import_paths : dict[str, str]
        Fixture used for test setup
    """

    mock_empty_response_object: dict[str, list[Any]] = {"response": []}
    empty_response = Response()
    empty_response._content = json.dumps(mock_empty_response_object).encode()

    # * Mock ApiLimitReached
    mocker.patch(import_paths["http_request"], return_value=empty_response)
    mocker.patch(import_paths["validate_api"], return_value=True)
    mocker.patch(import_paths["get_league_id"], return_value=1)

    with pytest.raises(ApiLimitReached, match="You have reached the handball API request limit for the day"):
        get_league_table("test_name")


# * ---------------------------------------------------------------------------

# * get_team_id ---------------------------------------------------------------
def test_get_team_id(mocker: MockFixture, import_paths: dict[str, str]) -> None:
    """Test `aswe.api.sport.handball.get_team_id`

    Parameters
    ----------
    mocker : MockFixture
    import_paths : dict[str, str]
        Fixture used for test setup
    """

    # * Mock valid response
    mock_valid_response_object = {"response": [{"id": "1"}]}
    valid_response = Response()
    valid_response._content = json.dumps(mock_valid_response_object).encode()
    mocker.patch(import_paths["http_request"], return_value=valid_response)
    mocker.patch(import_paths["validate_api"], return_value=False)

    assert get_team_id("test_name") == 1


def test_get_team_id_invalid_response(mocker: MockFixture, import_paths: dict[str, str]) -> None:
    """Test `aswe.api.sport.handball.get_team_id` with invalid api responses

    Parameters
    ----------
    mocker : MockFixture
    import_paths : dict[str, str]
        Fixture used for test setup
    """

    # * Mock None response
    mocker.patch(import_paths["http_request"], return_value=None)

    assert get_team_id("test_name") is None

    # * Mock empty response
    mock_valid_response_object = {"response": []}
    valid_response = Response()
    valid_response._content = json.dumps(mock_valid_response_object).encode()
    mocker.patch(import_paths["http_request"], return_value=valid_response)
    mocker.patch(import_paths["validate_api"], return_value=False)

    assert get_team_id("test_name") is None


def test_get_team_id_api_limit(mocker: MockFixture, import_paths: dict[str, str]) -> None:
    """Test `aswe.api.sport.handball.get_team_id` when Api limit has been reached

    Parameters
    ----------
    mocker : MockFixture
    import_paths : dict[str, str]
        Fixture used for test setup
    """

    mock_empty_response_object: dict[str, list[Any]] = {"response": []}
    empty_response = Response()
    empty_response._content = json.dumps(mock_empty_response_object).encode()

    # * Mock ApiLimitReached
    mocker.patch(import_paths["http_request"], return_value=empty_response)
    mocker.patch(import_paths["validate_api"], return_value=True)

    with pytest.raises(ApiLimitReached, match="You have reached the handball API request limit for the day"):
        get_team_id("test_team")


# * ---------------------------------------------------------------------------

# * get_team_game_today -------------------------------------------------------
def test_get_team_game_today(mocker: MockFixture, import_paths: dict[str, str]) -> None:
    """Test `aswe.api.sport.handball.get_team_game_today`

    Parameters
    ----------
    mocker : MockFixture
        _description_
    import_paths : dict[str, str]
        Fixture used for test setup
    """

    # * Mock valid response
    mock_valid_response_object = {
        "response": [
            {"teams": {"home": {"name": "test_home"}, "away": {"name": "test_away"}}, "scores": {"home": 1, "away": 2}}
        ]
    }
    valid_response = Response()
    valid_response._content = json.dumps(mock_valid_response_object).encode()
    mocker.patch(import_paths["http_request"], return_value=valid_response)
    mocker.patch(import_paths["validate_api"], return_value=False)
    mocker.patch(import_paths["get_league_id"], return_value=1)
    mocker.patch(import_paths["get_team_id"], return_value=1)

    assert get_team_game_today("test_name") == ["test_home 1 - 2 test_away"]


def test_get_team_game_today_invalid_response(mocker: MockFixture, import_paths: dict[str, str]) -> None:
    """Test `aswe.api.sport.handball.get_team_game_today` with invalid api responses

    Parameters
    ----------
    mocker : MockFixture
    import_paths : dict[str, str]
        Fixture used for test setup
    """
    # * Mock None league id
    mocker.patch(import_paths["get_league_id"], return_value=None)

    assert get_team_game_today("test_name") is None

    # * Mock None team id
    mocker.patch(import_paths["get_league_id"], return_value=1)
    mocker.patch(import_paths["get_team_id"], return_value=None)

    assert get_team_game_today("test_name") is None

    # * Mock None response
    mocker.patch(import_paths["get_team_id"], return_value=1)
    mocker.patch(import_paths["http_request"], return_value=None)

    assert get_team_game_today("test_name") is None

    # * Mock empty response
    mock_empty_response_object: dict[str, list[Any]] = {"response": []}
    empty_response = Response()
    empty_response._content = json.dumps(mock_empty_response_object).encode()

    mocker.patch(import_paths["http_request"], return_value=empty_response)

    assert get_team_game_today("test_name") == []


def test_get_team_game_today_api_limit(mocker: MockFixture, import_paths: dict[str, str]) -> None:
    """Test `aswe.api.sport.handball.get_team_game_today` when Api limit has been reached

    Parameters
    ----------
    mocker : MockFixture
    import_paths : dict[str, str]
        Fixture used for test setup
    """

    # * Mock ApiLimitReached
    mocker.patch(import_paths["http_request"], return_value=1)
    mocker.patch(import_paths["validate_api"], return_value=True)
    mocker.patch(import_paths["get_league_id"], return_value=1)
    mocker.patch(import_paths["get_team_id"], return_value=1)

    with pytest.raises(ApiLimitReached, match="You have reached the handball API request limit for the day"):
        get_team_game_today("test_team")


# * ---------------------------------------------------------------------------
