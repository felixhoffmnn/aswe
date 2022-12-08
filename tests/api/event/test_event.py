# ? Disable private attribute access to test class methods
# pylint: disable=redefined-outer-name,protected-access

import pytest
from pytest_mock import MockFixture
from requests.models import Response

from aswe.api.event import event as eventApi
from aswe.api.event.event_data import EventLocation, ReducedEvent
from aswe.api.event.event_params import EventApiEventParams


@pytest.fixture(scope="function")
def mock_event_api_key(mocker: MockFixture) -> None:
    """Returns new instance"""

    mocker.patch.object(eventApi, "_API_KEY", new="test_key")


def test_validate_api_key() -> None:
    """Test whether class checks for API key"""
    eventApi._API_KEY = ""
    with pytest.raises(Exception, match="EVENT_API_KEY was not loaded into system"):  # type: ignore
        eventApi._validate_api_key()


def test_reduce_events(mock_event_api_key: None) -> None:
    """Call `_reduce_events` with expected Http response and test for return values"""
    assert not eventApi._reduce_events({})

    test_events = {
        "_embedded": {
            "events": [
                {
                    "id": "test_id",
                    "name": "test_name",
                    "dates": {"status": {"code": "onsale"}, "start": {"dateTime": "2025-01-01T00:00:00Z"}},
                    "_embedded": {
                        "venues": [
                            {
                                "name": "test_venue_name",
                                "city": {"name": "test_city_name"},
                                "address": {"line1": "test_address"},
                            }
                        ]
                    },
                },
                {"dates": {"status": {"code": "offsale"}}},
                {"dates": {"status": {"code": "onsale"}}},
            ]
        }
    }

    reduced_event_list = eventApi._reduce_events(test_events)

    assert len(reduced_event_list) == 1

    assert reduced_event_list[0] == ReducedEvent(
        id="test_id",
        name="test_name",
        start="2025-01-01T01:00:00Z",
        status="onsale",
        location=EventLocation(name="test_venue_name", city="test_city_name", address="test_address"),
    )


def test_events_invalid_params(mock_event_api_key: None) -> None:
    """Test `events` class method. Call function with invalid params."""

    with pytest.raises(Exception, match="Given Event Api Event Params are invalid"):
        invalid_event_params = EventApiEventParams(radius=0)
        eventApi.events(invalid_event_params)


def test_events_valid_response(mock_event_api_key: None, mocker: MockFixture) -> None:
    """Test `events` class method. Call function with valid params.
    Mocked functions:
        - `http_request`"""
    http_import_path = "aswe.api.event.event.http_request"

    # * Mock valid response
    valid_response = Response()
    valid_response._content = b'{"lorem": "ipsum"}'
    valid_response.status_code = 200
    mocker.patch(http_import_path, return_value=valid_response)
    actual_response = eventApi.events(EventApiEventParams())

    assert actual_response == []

    # * Mock JSONDecodeError
    invalid_response = Response()
    invalid_response._content = b'{"lorem": "ipsum}'
    invalid_response.status_code = 200
    mocker.patch(http_import_path, return_value=invalid_response)
    actual_response = eventApi.events(EventApiEventParams())

    assert actual_response is None

    # * Mock other Exception
    mocker.patch(http_import_path, return_value=False)
    actual_response = eventApi.events(EventApiEventParams())

    assert actual_response is None
