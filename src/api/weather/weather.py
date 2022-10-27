import os
from datetime import datetime
from typing import Any, Final

from loguru import logger
from requests import JSONDecodeError

from src.api.weather.weather_params import WeatherApiParams
from src.utils.http_request import http_request
from src.utils.validate_date import validate_date


class WeatherApi:
    """Crawler Class retrieves data from the [Visual Crossing API](https://www.visualcrossing.com/)"""

    _BASE_URL: Final[str] = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
    _API_KEY: Final[str] = os.getenv("WEATHER_API_KEY", "")

    PARAMS: Final[WeatherApiParams] = WeatherApiParams()
    UNIT_GROUP: Final[str] = "metric"
    'Defines unit system data is converted to. "metric" or "us". Defaults to "metric"'

    def __init__(self) -> None:
        self._validate_api_key()

    def _validate_api_key(self) -> None:
        if self._API_KEY == "":
            raise Exception("WEATHER_API_KEY was not loaded into system")

    def _validate_api_params(
        self,
        include: list[WeatherApiParams.INCLUDE] | None = None,
        elements: list[WeatherApiParams.ELEMENTS] | None = None,
    ) -> bool:
        if include is not None:
            for param in include:
                if not WeatherApiParams.INCLUDE.has_value(param):
                    logger.error(f"WeatherApiParams.INCLUDE value is invalid: {param}")
                    return False

        if elements is not None:
            for param in elements:
                if not WeatherApiParams.ELEMENTS.has_value(param):
                    logger.error(f"Element value is invalid: {param}")
                    return False

        return True

    def _validate_location(self, location: str) -> bool:
        try:
            city, country = location.split(",")

            if city != "" and len(country) == 2:
                return True

            logger.error(f"Country code of location is invalid: {location}")

        except Exception:
            logger.error(f"Location seems to be invalid: {location}")

        return False

    def _append_api_params(
        self,
        url: str,
        elements: list[WeatherApiParams.ELEMENTS] | None = None,
        include: list[WeatherApiParams.INCLUDE] | None = None,
    ) -> str:
        if elements is not None:
            url += f"""&elements={",".join(elements)}"""

        if include is not None:
            url += f"""&include={",".join(include)}"""

        return url

    def historic_range(
        self,
        location: str,
        start_date: str,
        end_date: str,
        elements: list[WeatherApiParams.ELEMENTS] | None = None,
        include: list[WeatherApiParams.INCLUDE] | None = None,
    ) -> dict[Any, Any] | None:
        """Retrieves historic data between two given dates.

        Args:
            location (str): Location format: "city, country" Country needs to be in\
            [Alpha-2](https://www.iban.com/country-codes) Code.

            start_date (str): Date format: "YYYY-MM-DD", Optional: "YYYY-MM-DDThhmm:ss".

            end_date (str): Date format: "YYYY-MM-DD", Optional: "YYYY-MM-DDThhmm:ss".

            elements (list[WeatherApiParams.ELEMENTS] | None, optional): List of possible properties in a
            day or hourly data object that should be retrieved from the API. Refer to `weather_params.py`.
            Defaults to None.

            include (list[WeatherApiParams.INCLUDE] | None, optional): List of possible information that
            should be retrieved from the API. Refer to `weather_params.py`. Defaults to None.
        """

        location = location.replace(" ", "")

        if not self._validate_location(location):
            raise Exception("Given location is invalid")

        if not validate_date(start_date):
            raise Exception("Given start_date is invalid")

        if not validate_date(end_date):
            raise Exception("Given end_date is invalid")

        if end_date < start_date:
            raise Exception("end_date must be greater than start_date")

        today = datetime.today().strftime("%Y-%m-%d")

        if today <= end_date:
            raise Exception("end_date must be less than current date")

        if not self._validate_api_params(include, elements):
            raise Exception("Given API params are invalid")

        url = f"""{self._BASE_URL}/{location}/{start_date}/{end_date}?key={self._API_KEY}&unitGroup={self.UNIT_GROUP}"""

        url = self._append_api_params(url, elements, include)

        response = http_request(url)

        try:
            response_json = dict(response.json())
            return response_json

        except JSONDecodeError as err:
            logger.error(f"Weather API returned invalid Json: {err}")
        except Exception as err:
            logger.error(f"Something went wrong: {err}")

        return None

    def historic_day(
        self,
        location: str,
        date: str,
        elements: list[WeatherApiParams.ELEMENTS] | None = None,
        include: list[WeatherApiParams.INCLUDE] | None = None,
    ) -> dict[Any, Any] | None:
        """Retrieves historic data from a specific day.

        Args:
            location (str): Location format: "city, country" Country needs to be in\
            [Alpha-2](https://www.iban.com/country-codes) Code.

            date (str): Date format: "YYYY-MM-DD", Optional: "YYYY-MM-DDThhmm:ss".

            elements (list[WeatherApiParams.ELEMENTS] | None, optional): List of possible properties
            in a day or hourly data object that should be retrieved from the API. Refer to `weather_params.py`.
            Defaults to None.

            include (list[WeatherApiParams.INCLUDE] | None, optional): List of possible information
            that should be retrieved from the API. Refer to `weather_params.py`. Defaults to None.
        """
        location = location.replace(" ", "")

        if not self._validate_location(location):
            raise Exception("Given location is invalid")

        if not validate_date(date):
            raise Exception("Given date is invalid")

        today = datetime.today().strftime("%Y-%m-%d")

        if today <= date:
            raise Exception("Given day must be less than current date")

        if not self._validate_api_params(include, elements):
            raise Exception("Given API params are invalid")

        url = f"""{self._BASE_URL}/{location}/{date}?key={self._API_KEY}&unitGroup={self.UNIT_GROUP}"""

        url = self._append_api_params(url, elements, include)

        response = http_request(url)

        try:
            response_json = dict(response.json())
            return response_json

        except JSONDecodeError as err:
            logger.error(f"Weather API returned invalid Json: {err}")
        except Exception as err:
            logger.error(f"Something went wrong: {err}")

        return None

    # TODO next_x_days is inclusive with today, adapt docstring
    def dynamic_range(
        self,
        location: str,
        dynamic_period: WeatherApiParams.DYNAMIC_PERIOD,
        elements: list[WeatherApiParams.ELEMENTS] | None = None,
        include: list[WeatherApiParams.INCLUDE] | None = None,
    ) -> dict[Any, Any] | None:
        """Retrieves dynamic data relative to current date

        Args:
            location (str): Location format: "city, country" Country needs to be in\
            [Alpha-2](https://www.iban.com/country-codes) Code.

            dynamic_period (WeatherApiParams.DYNAMIC_PERIOD): Dynamic Period. Refer to `weather_params.py`.

            elements (list[WeatherApiParams.ELEMENTS] | None, optional): List of possible properties in a day
            or hourly data object that should be retrieved from the API. Refer to `weather_params.py`.
            Defaults to None.

            include (list[WeatherApiParams.INCLUDE] | None, optional): List of possible information that
            should be retrieved from the API. Refer to `weather_params.py`.
            Defaults to None.
        """

        location = location.replace(" ", "")

        if not self._validate_location(location):
            raise Exception("Given location is invalid")

        if not WeatherApiParams.DYNAMIC_PERIOD.has_value(dynamic_period):
            raise Exception("Given WeatherApiParams.DYNAMIC_PERIOD is invalid")

        if not self._validate_api_params(include, elements):
            raise Exception("Given API params are invalid")

        url = f"""{self._BASE_URL}/{location}/{dynamic_period}?key={self._API_KEY}&unitGroup={self.UNIT_GROUP}"""

        url = self._append_api_params(url, elements, include)

        response = http_request(url)

        try:
            response_json = dict(response.json())
            return response_json

        except JSONDecodeError as err:
            logger.error(f"Weather API returned invalid Json: {err}")
        except Exception as err:
            logger.error(f"Something went wrong: {err}")

        return None

    def forecast(
        self,
        location: str,
        elements: list[WeatherApiParams.ELEMENTS] | None = None,
        include: list[WeatherApiParams.INCLUDE] | None = None,
    ) -> dict[Any, Any] | None:
        """Retrieves 15-day weather forecast of given location

        Args:
            location (str): Location format: "city, country" Country needs to be in\
            [Alpha-2](https://www.iban.com/country-codes) Code.

            elements (list[WeatherApiParams.ELEMENTS] | None, optional): List of possible properties in
            a day or hourly data object that should be retrieved from the API. Refer to `weather_params.py`.
            Defaults to None.

            include (list[WeatherApiParams.INCLUDE] | None, optional): List of possible information that
            should be retrieved from the API. Refer to `weather_params.py`.
            Defaults to None.
        """

        location = location.replace(" ", "")

        if not self._validate_location(location):
            raise Exception("Given location is invalid")

        if not self._validate_api_params(include, elements):
            raise Exception("Given API params are invalid")

        url = f"""{self._BASE_URL}/{location}?key={self._API_KEY}&unitGroup={self.UNIT_GROUP}"""

        url = self._append_api_params(url, elements, include)

        response = http_request(url)

        try:
            response_json = dict(response.json())
            return response_json

        except JSONDecodeError as err:
            logger.error(f"Weather API returned invalid JSON: {err}")
        except Exception as err:
            logger.error(f"Something went wrong: {err}")

        return None
