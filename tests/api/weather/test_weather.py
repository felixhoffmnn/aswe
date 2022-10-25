# ? Disable typing errors for pytest fixtures
# ? Disable private attribute access to test class methods
# pylint: disable=redefined-outer-name,protected-access


import pytest
from pytest_mock import MockFixture
from requests.models import Response

from src.api.weather.weather import WeatherApi
from src.api.weather.weather_params import DynamicPeriod, Elements, Include


@pytest.fixture(scope="function")
def weather_api_instance() -> WeatherApi:
    """Returns new instance"""

    WeatherApi._API_KEY = "test_key"
    return WeatherApi()


def test_constants(weather_api_instance: WeatherApi) -> None:
    """Test Class Constants"""

    assert weather_api_instance.UNIT_GROUP == "metric"


def test_class_init() -> None:
    """Test `__init__` class method"""

    WeatherApi._API_KEY = ""
    with pytest.raises(Exception, match="WEATHER_API_KEY was not loaded into system"):
        WeatherApi()


def test_validate_api_params(weather_api_instance: WeatherApi) -> None:
    """Test `_validate_api_params` class method"""

    assert weather_api_instance._validate_api_params(["lorem"]) is False
    assert weather_api_instance._validate_api_params(None, ["lorem"]) is False
    assert weather_api_instance._validate_api_params([Include.ALERTS], [Elements.CAPE]) is True


def test_validate_location(weather_api_instance: WeatherApi) -> None:
    """Test `_validate_location` class method"""

    assert weather_api_instance._validate_location("") is False
    assert weather_api_instance._validate_location("Lorem,") is False
    assert weather_api_instance._validate_location(",Ipsum") is False
    assert weather_api_instance._validate_location("Lorem,Ipsum") is False
    assert weather_api_instance._validate_location("Lorem,IP") is True


def test_append_api_params(weather_api_instance: WeatherApi) -> None:
    """Test `_append_api_params` class method"""

    base_url = "lorem.ipsum.com"
    assert weather_api_instance._append_api_params(base_url, None, None) == base_url
    assert (
        weather_api_instance._append_api_params(base_url, None, [Include.ALERTS, Include.CURRENT])
        == f"{base_url}&include=alerts,current"
    )
    assert (
        weather_api_instance._append_api_params(base_url, [Elements.CAPE, Elements.CIN], None)
        == f"{base_url}&elements=cape,cin"
    )
    assert (
        weather_api_instance._append_api_params(base_url, [Elements.CAPE], [Include.ALERTS])
        == f"{base_url}&elements=cape&include=alerts"
    )


def test_historic_range_invalid_params(weather_api_instance: WeatherApi) -> None:
    """Test `historic_range` class method. Call method with invalid params"""

    with pytest.raises(Exception, match="Given location is invalid"):
        weather_api_instance.historic_range("Lorem,Ipsum", "", "")

    with pytest.raises(Exception, match="Given start_date is invalid"):
        weather_api_instance.historic_range("Lorem,Ip", "", "")

    with pytest.raises(Exception, match="Given end_date is invalid"):
        weather_api_instance.historic_range("Lorem,Ip", "2022-01-01", "")

    with pytest.raises(Exception, match="end_date must be greater than start_date"):
        weather_api_instance.historic_range("Lorem,Ip", "2022-01-01", "2021-01-01")

    with pytest.raises(Exception, match="end_date must be less than current date"):
        weather_api_instance.historic_range("Lorem,Ip", "2022-01-01", "2050-01-01")

    with pytest.raises(Exception, match="Given API params are invalid"):
        weather_api_instance.historic_range("Lorem,Ip", "2022-01-01", "2022-02-02", ["lorem"], ["ipsum"])


def test_historic_range_valid_params(weather_api_instance: WeatherApi, mocker: MockFixture) -> None:
    """Test `historic_range` class method. Call function with valid params.
    Mocked functions:
        - `http_request`"""

    http_import_path = "src.api.weather.weather.http_request"

    # * Mock valid response
    valid_response = Response()
    valid_response._content = b'{"lorem": "ipsum"}'
    mocker.patch(http_import_path, return_value=valid_response)
    actual_response = weather_api_instance.historic_range("Lorem,Ip", "2022-01-01", "2022-02-02")

    assert {"lorem": "ipsum"} == actual_response

    # * Mock JSONDecodeError
    invalid_response = Response()
    invalid_response._content = b'{"lorem": "ipsum}'
    mocker.patch(http_import_path, return_value=invalid_response)
    actual_response = weather_api_instance.historic_range("Lorem,Ip", "2022-01-01", "2022-02-02")

    assert actual_response is None

    # * Mock other Exception
    mocker.patch(http_import_path, return_value=False)
    actual_response = weather_api_instance.historic_range("Lorem,Ip", "2022-01-01", "2022-02-02")

    assert actual_response is None


def test_historic_day_invalid_params(weather_api_instance: WeatherApi) -> None:
    """Test `historic_day` class method. Call method with invalid params"""

    with pytest.raises(Exception, match="Given location is invalid"):
        weather_api_instance.historic_day("Lorem,Ipsum", "")

    with pytest.raises(Exception, match="Given date is invalid"):
        weather_api_instance.historic_day("Lorem,Ip", "")

    with pytest.raises(Exception, match="Given day must be less than current date"):
        weather_api_instance.historic_day("Lorem,Ip", "2050-01-01")

    with pytest.raises(Exception, match="Given API params are invalid"):
        weather_api_instance.historic_day("Lorem,Ip", "2022-01-01", ["lorem"], ["ipsum"])


def test_historic_day_valid_params(weather_api_instance: WeatherApi, mocker: MockFixture) -> None:
    """Test `historic_day` class method. Call function with valid params.
    Mocked functions:
        - `http_request`"""

    http_import_path = "src.api.weather.weather.http_request"

    # * Mock valid response
    valid_response = Response()
    valid_response._content = b'{"lorem": "ipsum"}'
    mocker.patch(http_import_path, return_value=valid_response)
    actual_response = weather_api_instance.historic_day("Lorem,Ip", "2022-01-01")

    assert {"lorem": "ipsum"} == actual_response

    # * Mock JSONDecodeError
    invalid_response = Response()
    invalid_response._content = b'{"lorem": "ipsum}'
    mocker.patch(http_import_path, return_value=invalid_response)
    actual_response = weather_api_instance.historic_day("Lorem,Ip", "2022-01-01")

    assert actual_response is None

    # * Mock other Exception
    mocker.patch(http_import_path, return_value=False)
    actual_response = weather_api_instance.historic_day("Lorem,Ip", "2022-01-01")

    assert actual_response is None


def test_dynamic_range_invalid_params(weather_api_instance: WeatherApi) -> None:
    """Test `dynamic_range` class method. Call method with invalid params"""

    with pytest.raises(Exception, match="Given location is invalid"):
        weather_api_instance.dynamic_range("Lorem,Ipsum", "")

    with pytest.raises(Exception, match="Given DynamicPeriod is invalid"):
        weather_api_instance.dynamic_range("Lorem,Ip", "lorem")

    with pytest.raises(Exception, match="Given API params are invalid"):
        weather_api_instance.dynamic_range("Lorem,Ip", DynamicPeriod.TODAY, ["lorem"], ["ipsum"])


def test_dynamic_range_valid_params(weather_api_instance: WeatherApi, mocker: MockFixture) -> None:
    """Test `dynamic_range` class method. Call function with valid params.
    Mocked functions:
        - `http_request`"""

    http_import_path = "src.api.weather.weather.http_request"

    # * Mock valid response
    valid_response = Response()
    valid_response._content = b'{"lorem": "ipsum"}'
    mocker.patch(http_import_path, return_value=valid_response)
    actual_response = weather_api_instance.dynamic_range("Lorem,Ip", DynamicPeriod.TODAY)

    assert {"lorem": "ipsum"} == actual_response

    # * Mock JSONDecodeError
    invalid_response = Response()
    invalid_response._content = b'{"lorem": "ipsum}'
    mocker.patch(http_import_path, return_value=invalid_response)
    actual_response = weather_api_instance.dynamic_range("Lorem,Ip", DynamicPeriod.TODAY)

    assert actual_response is None

    # * Mock other Exception
    mocker.patch(http_import_path, return_value=False)
    actual_response = weather_api_instance.dynamic_range("Lorem,Ip", DynamicPeriod.TODAY)

    assert actual_response is None


def test_forecast_invalid_params(weather_api_instance: WeatherApi) -> None:
    """Test `forecast` class method. Call method with invalid params"""

    with pytest.raises(Exception, match="Given location is invalid"):
        weather_api_instance.forecast("Lorem,Ipsum")

    with pytest.raises(Exception, match="Given API params are invalid"):
        weather_api_instance.forecast("Lorem,Ip", ["lorem"], ["ipsum"])


def test_forecast_valid_params(weather_api_instance: WeatherApi, mocker: MockFixture) -> None:
    """Test `forecast` class method. Call function with valid params.
    Mocked functions:
        - `http_request`"""

    http_import_path = "src.api.weather.weather.http_request"

    # * Mock valid response
    valid_response = Response()
    valid_response._content = b'{"lorem": "ipsum"}'
    mocker.patch(http_import_path, return_value=valid_response)
    actual_response = weather_api_instance.forecast("Lorem,Ip")

    assert {"lorem": "ipsum"} == actual_response

    # * Mock JSONDecodeError
    invalid_response = Response()
    invalid_response._content = b'{"lorem": "ipsum}'
    mocker.patch(http_import_path, return_value=invalid_response)
    actual_response = weather_api_instance.forecast("Lorem,Ip")

    assert actual_response is None

    # * Mock other Exception
    mocker.patch(http_import_path, return_value=False)
    actual_response = weather_api_instance.forecast("Lorem,Ip")

    assert actual_response is None
