# ? Disable typing errors for pytest fixtures
# ? Disable private attribute access to test class methods
# pylint: disable=redefined-outer-name,protected-access


import pytest
from pytest_mock import MockFixture
from requests.models import Response

from aswe.api.weather.weather import WeatherApi
from aswe.api.weather.weather_params import DynamicPeriodEnum, ElementsEnum, IncludeEnum


@pytest.fixture(scope="function")
def weather_api() -> WeatherApi:
    """Returns new instance"""

    WeatherApi._API_KEY = "test_key"
    return WeatherApi()


def test_constants(weather_api: WeatherApi) -> None:
    """Test Class Constants"""

    assert weather_api.UNIT_GROUP == "metric"


def test_class_init() -> None:
    """Test `__init__` class method"""

    WeatherApi._API_KEY = ""
    with pytest.raises(Exception, match="WEATHER_API_KEY was not loaded into system"):
        WeatherApi()


# TODO:
# def test_validate_api_params(weather_api: WeatherApi) -> None:
#     """Test `_validate_api_params` class method"""

#     assert weather_api._validate_api_params(["lorem"]) is False  # type: ignore
#     assert weather_api._validate_api_params(None, ["lorem"]) is False  # type: ignore
#     assert weather_api._validate_api_params([IncludeEnum.ALERTS], [ElementsEnum.CAPE]) is True


def test_validate_location(weather_api: WeatherApi) -> None:
    """Test `_validate_location` class method"""

    assert weather_api._validate_location("") is False
    assert weather_api._validate_location("Lorem,") is False
    assert weather_api._validate_location(",Ipsum") is False
    assert weather_api._validate_location("Lorem,Ipsum") is False
    assert weather_api._validate_location("Lorem,IP") is True


def test_append_api_params(weather_api: WeatherApi) -> None:
    """Test `_append_api_params` class method"""

    base_url = "lorem.ipsum.com"
    assert weather_api._append_api_params(base_url, None, None) == base_url
    assert (
        weather_api._append_api_params(base_url, [IncludeEnum.ALERTS, IncludeEnum.CURRENT])
        == f"{base_url}&include=alerts,current"
    )
    assert (
        weather_api._append_api_params(base_url, None, [ElementsEnum.CAPE, ElementsEnum.CIN])
        == f"{base_url}&elements=cape,cin"
    )
    assert (
        weather_api._append_api_params(base_url, [IncludeEnum.ALERTS], [ElementsEnum.CAPE])
        == f"{base_url}&elements=cape&include=alerts"
    )


def test_historic_range_invalid_params(weather_api: WeatherApi) -> None:
    """Test `historic_range` class method. Call method with invalid params"""

    with pytest.raises(Exception, match="Given location is invalid"):
        weather_api.historic_range("Lorem,Ipsum", "", "")

    with pytest.raises(Exception, match="Given start_date is invalid"):
        weather_api.historic_range("Lorem,Ip", "", "")

    with pytest.raises(Exception, match="Given end_date is invalid"):
        weather_api.historic_range("Lorem,Ip", "2022-01-01", "")

    with pytest.raises(Exception, match="end_date must be greater than start_date"):
        weather_api.historic_range("Lorem,Ip", "2022-01-01", "2021-01-01")

    with pytest.raises(Exception, match="end_date must be less than current date"):
        weather_api.historic_range("Lorem,Ip", "2022-01-01", "2050-01-01")

    with pytest.raises(AttributeError):
        weather_api.historic_range("Lorem,Ip", "2022-01-01", "2022-02-02", ["lorem"], ["ipsum"])  # type: ignore


def test_historic_range_valid_params(weather_api: WeatherApi, mocker: MockFixture) -> None:
    """Test `historic_range` class method. Call function with valid params.
    Mocked functions:
        - `http_request`"""

    http_import_path = "aswe.api.weather.weather.http_request"

    # * Mock valid response
    valid_response = Response()
    valid_response._content = b'{"lorem": "ipsum"}'
    mocker.patch(http_import_path, return_value=valid_response)
    actual_response = weather_api.historic_range("Lorem,Ip", "2022-01-01", "2022-02-02")

    assert {"lorem": "ipsum"} == actual_response

    # * Mock JSONDecodeError
    invalid_response = Response()
    invalid_response._content = b'{"lorem": "ipsum}'
    mocker.patch(http_import_path, return_value=invalid_response)
    actual_response = weather_api.historic_range("Lorem,Ip", "2022-01-01", "2022-02-02")

    assert actual_response is None

    # * Mock other Exception
    mocker.patch(http_import_path, return_value=False)
    actual_response = weather_api.historic_range("Lorem,Ip", "2022-01-01", "2022-02-02")

    assert actual_response is None


def test_historic_day_invalid_params(weather_api: WeatherApi) -> None:
    """Test `historic_day` class method. Call method with invalid params"""

    with pytest.raises(Exception, match="Given location is invalid"):
        weather_api.historic_day("Lorem,Ipsum", "")

    with pytest.raises(Exception, match="Given date is invalid"):
        weather_api.historic_day("Lorem,Ip", "")

    with pytest.raises(Exception, match="Given day must be less than current date"):
        weather_api.historic_day("Lorem,Ip", "2050-01-01")

    with pytest.raises(AttributeError):
        weather_api.historic_day("Lorem,Ip", "2022-01-01", ["lorem"], ["ipsum"])  # type: ignore


def test_historic_day_valid_params(weather_api: WeatherApi, mocker: MockFixture) -> None:
    """Test `historic_day` class method. Call function with valid params.
    Mocked functions:
        - `http_request`"""

    http_import_path = "aswe.api.weather.weather.http_request"

    # * Mock valid response
    valid_response = Response()
    valid_response._content = b'{"lorem": "ipsum"}'
    mocker.patch(http_import_path, return_value=valid_response)
    actual_response = weather_api.historic_day("Lorem,Ip", "2022-01-01")

    assert {"lorem": "ipsum"} == actual_response

    # * Mock JSONDecodeError
    invalid_response = Response()
    invalid_response._content = b'{"lorem": "ipsum}'
    mocker.patch(http_import_path, return_value=invalid_response)
    actual_response = weather_api.historic_day("Lorem,Ip", "2022-01-01")

    assert actual_response is None

    # * Mock other Exception
    mocker.patch(http_import_path, return_value=False)
    actual_response = weather_api.historic_day("Lorem,Ip", "2022-01-01")

    assert actual_response is None


def test_dynamic_range_invalid_params(weather_api: WeatherApi) -> None:
    """Test `dynamic_range` class method. Call method with invalid params"""

    with pytest.raises(Exception, match="Given location is invalid"):
        weather_api.dynamic_range("Lorem,Ipsum", "")  # type: ignore

    with pytest.raises(AttributeError):
        weather_api.dynamic_range("Lorem,Ip", "lorem")  # type: ignore

    with pytest.raises(AttributeError):
        weather_api.dynamic_range("Lorem,Ip", DynamicPeriodEnum.TODAY, ["lorem"], ["ipsum"])  # type: ignore


def test_dynamic_range_valid_params(weather_api: WeatherApi, mocker: MockFixture) -> None:
    """Test `dynamic_range` class method. Call function with valid params.
    Mocked functions:
        - `http_request`"""

    http_import_path = "aswe.api.weather.weather.http_request"

    # * Mock valid response
    valid_response = Response()
    valid_response._content = b'{"lorem": "ipsum"}'
    mocker.patch(http_import_path, return_value=valid_response)
    actual_response = weather_api.dynamic_range("Lorem,Ip", DynamicPeriodEnum.TODAY)

    assert {"lorem": "ipsum"} == actual_response

    # * Mock JSONDecodeError
    invalid_response = Response()
    invalid_response._content = b'{"lorem": "ipsum}'
    mocker.patch(http_import_path, return_value=invalid_response)
    actual_response = weather_api.dynamic_range("Lorem,Ip", DynamicPeriodEnum.TODAY)

    assert actual_response is None

    # * Mock other Exception
    mocker.patch(http_import_path, return_value=False)
    actual_response = weather_api.dynamic_range("Lorem,Ip", DynamicPeriodEnum.TODAY)

    assert actual_response is None


def test_forecast_invalid_params(weather_api: WeatherApi) -> None:
    """Test `forecast` class method. Call method with invalid params"""

    with pytest.raises(Exception, match="Given location is invalid"):
        weather_api.forecast("Lorem,Ipsum")

    # TODO: Correct typing should already prevent this behavior
    with pytest.raises(AttributeError):
        weather_api.forecast("Lorem,Ip", ["lorem"], ["ipsum"])  # type: ignore


def test_forecast_valid_params(weather_api: WeatherApi, mocker: MockFixture) -> None:
    """Test `forecast` class method. Call function with valid params.
    Mocked functions:
        - `http_request`"""

    http_import_path = "aswe.api.weather.weather.http_request"

    # * Mock valid response
    valid_response = Response()
    valid_response._content = b'{"lorem": "ipsum"}'
    mocker.patch(http_import_path, return_value=valid_response)
    actual_response = weather_api.forecast("Lorem,Ip")

    assert {"lorem": "ipsum"} == actual_response

    # * Mock JSONDecodeError
    invalid_response = Response()
    invalid_response._content = b'{"lorem": "ipsum}'
    mocker.patch(http_import_path, return_value=invalid_response)
    actual_response = weather_api.forecast("Lorem,Ip")

    assert actual_response is None

    # * Mock other Exception
    mocker.patch(http_import_path, return_value=False)
    actual_response = weather_api.forecast("Lorem,Ip")

    assert actual_response is None
