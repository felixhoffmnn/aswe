# ? Disable typing errors for pytest fixtures
# ? Disable private attribute access to test class methods
# pylint: disable=redefined-outer-name,protected-access

import json

import pytest
from pytest_mock import MockFixture
from requests.models import Response

from aswe.api.news.news import keyword_search, top_headlines_search


@pytest.fixture
def import_paths() -> dict[str, str]:
    """Prepare import paths of functions which shall be mocked"""

    return {
        "http_request": "aswe.api.news.news.http_request",
    }


# * top_headlines_search ------------------------------------------------------
def test_top_headlines_search(mocker: MockFixture, import_paths: dict[str, str]) -> None:
    """Test `aswe.api.news.news.test_top_headlines_search`

    Parameters
    ----------
    mocker : MockFixture
    import_paths : dict[str, str]
        Fixture used for test setup
    """
    # * Mock valid response
    mock_valid_response_object_1 = {"articles": [{"title": "test_title", "description": "test_description"}]}
    valid_response = Response()
    valid_response._content = json.dumps(mock_valid_response_object_1).encode()
    mocker.patch(import_paths["http_request"], return_value=valid_response)

    assert top_headlines_search() == ["test_title: test_description"]

    mock_valid_response_object_2: dict[str, list[dict[str, str | None]]] = {
        "articles": [{"title": "test_title", "description": None}]
    }
    valid_response = Response()
    valid_response._content = json.dumps(mock_valid_response_object_2).encode()
    mocker.patch(import_paths["http_request"], return_value=valid_response)

    assert top_headlines_search() == ["test_title"]


def test_top_headlines_search_empty_response(mocker: MockFixture, import_paths: dict[str, str]) -> None:
    """Test `aswe.api.news.news.test_top_headlines_search` with and empty api response

    Parameters
    ----------
    mocker : MockFixture
    import_paths : dict[str, str]
        Fixture used for test setup
    """

    # * Mock None response
    mocker.patch(import_paths["http_request"], return_value=None)

    assert top_headlines_search() is None


# * ---------------------------------------------------------------------------


# * keyword_search ------------------------------------------------------------
def test_keyword_search(mocker: MockFixture, import_paths: dict[str, str]) -> None:
    """Test `aswe.api.sport.handball.keyword_search`

    Parameters
    ----------
    mocker : MockFixture
    import_paths : dict[str, str]
        Fixture used for test setup
    """

    # * Mock valid response
    mock_valid_response_object = {"articles": [{"title": "test_title", "description": "test_description"}]}
    valid_response = Response()
    valid_response._content = json.dumps(mock_valid_response_object).encode()
    mocker.patch(import_paths["http_request"], return_value=valid_response)

    assert keyword_search("test_keyword") == ["test_title: test_description"]


def test_keyword_search_empty_response(mocker: MockFixture, import_paths: dict[str, str]) -> None:
    """Test `aswe.api.sport.handball.keyword_search` with and empty api response

    Parameters
    ----------
    mocker : MockFixture
    import_paths : dict[str, str]
        Fixture used for test setup
    """

    # * Mock None response
    mocker.patch(import_paths["http_request"], return_value=None)

    assert keyword_search("test_keyword") is None


# * ---------------------------------------------------------------------------
