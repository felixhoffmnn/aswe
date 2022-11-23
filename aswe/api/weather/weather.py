import os
from datetime import datetime
from typing import Any, Final

from loguru import logger
from requests import JSONDecodeError

from aswe.api.weather.weather_params import DynamicPeriodEnum, ElementsEnum, IncludeEnum
from aswe.utils.request import http_request
from aswe.utils.validate import validate_date


class WeatherApi:
    """Crawler Class retrieves data from the [Visual Crossing API](https://www.visualcrossing.com/)

    * TODO: Fix the wired typing and errors
    * TODO: Add docstrings
    """

    _BASE_URL: Final[str] = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
    _API_KEY: str = os.getenv("WEATHER_API_KEY", "")

    UNIT_GROUP: Final[str] = "metric"
    'Defines unit system data is converted to. "metric" or "us". Defaults to "metric"'

    def __init__(self) -> None:
        self._validate_api_key()

    def _validate_api_key(self) -> None:
        if self._API_KEY == "":
            raise Exception("WEATHER_API_KEY was not loaded into system")

    def _validate_api_params(
        self,
        include: list[IncludeEnum] | None = None,
        elements: list[ElementsEnum] | None = None,
    ) -> bool:
        if include is not None:
            for param in include:
                if not IncludeEnum.has_value(param.value):
                    logger.error(f"IncludeEnum value is invalid: {param}")
                    return False

        if elements is not None:
            for param in elements:  # type: ignore
                if not ElementsEnum.has_value(param.value):
                    logger.error(f"Element value is invalid: {param}")
                    return False

        return True

    def _validate_location(self, location: str) -> bool:
        try:
            city, country = location.split(",")

            if city != "" and len(country) == 2:
                return True
        except ValueError:
            logger.error(f"Country code of location is invalid: {location}")

        return False

    def _append_api_params(
        self,
        url: str,
        include: list[IncludeEnum] | None = None,
        elements: list[ElementsEnum] | None = None,
    ) -> str:
        """Appends API params to URL

        Parameters
        ----------
        url : str
            The URL to append the params to.
        include : list[IncludeEnum] | None, optional
            The list of IncludeEnum values to append to the URL. _By default `None`_.
        elements : list[ElementsEnum] | None, optional
            The list of ElementsEnum values to append to the URL. _By default `None`_.

        Returns
        -------
        str
            The URL with the appended params.
        """
        if elements is not None:
            url += f"&elements={','.join([elements.value for elements in elements])}"

        if include is not None:
            url += f"&include={','.join([include.value for include in include])}"

        return url

    def historic_range(
        self,
        location: str,
        start_date: str,
        end_date: str,
        include: list[IncludeEnum] | None = None,
        elements: list[ElementsEnum] | None = None,
    ) -> dict[Any, Any] | None:
        """Retrieves historic data between two given dates.

        Parameters
        ----------
        location : str
            Location format: "city, country" Country needs to be in [Alpha-2](https://www.iban.com/country-codes) Code.
        start_date : str
            Date format: `YYYY-MM-DD`, Optional: `YYYY-MM-DDThh:mm:ss`.
        end_date : str
            Date format: `YYYY-MM-DD`, Optional: `YYYY-MM-DDThh:mm:ss`.
        elements : list[ElementsEnum] | None, optional
            List of possible properties in a day or hourly data object that should be retrieved from the API. Refer to `weather_params.py`. _By default `None`_.
        include : list[IncludeEnum] | None, optional
            List of possible information that should be retrieved from the API. Refer to `weather_params.py`. _By default `None`_.
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

        today = datetime.today().strftime("%Y-%m-%d")  # type: ignore

        if today <= end_date:
            raise Exception("end_date must be less than current date")

        if not self._validate_api_params(include, elements):
            raise Exception("Given API params are invalid")

        url = f"{self._BASE_URL}/{location}/{start_date}/{end_date}?key={self._API_KEY}&unitGroup={self.UNIT_GROUP}"

        url = self._append_api_params(url, include, elements)

        response = http_request(url)

        if response is not None:
            try:
                response_json: dict[str, Any] = response.json()
                return response_json
            except (AttributeError, JSONDecodeError):
                logger.error("Weather API returned invalid JSON")

        return None

    def historic_day(
        self,
        location: str,
        date: str,
        include: list[IncludeEnum] | None = None,
        elements: list[ElementsEnum] | None = None,
    ) -> dict[Any, Any] | None:
        """Retrieves historic data from a specific day.

        Parameters
        ----------
        location : str
            Location format: "city, country" Country needs to be in [Alpha-2](https://www.iban.com/country-codes) Code.
        date : str
            Date format: `YYYY-MM-DD`, Optional: `YYYY-MM-DDThh:mm:ss`.
        elements : list[ElementsEnum] | None, optional
            List of possible properties in a day or hourly data object that should be retrieved from the API. Refer to `weather_params.py`. _By default `None`_.
        include : list[IncludeEnum] | None, optional
            List of possible information that should be retrieved from the API. Refer to `weather_params.py`. _By default `None`_.
        """
        location = location.replace(" ", "")

        if not self._validate_location(location):
            raise Exception("Given location is invalid")

        if not validate_date(date):
            raise Exception("Given date is invalid")

        today = datetime.today().strftime("%Y-%m-%d")

        if today <= date:
            raise Exception("Given day must be less than current date")

        # if not self._validate_api_params(include, elements):
        #     raise Exception("Given API params are invalid")

        url = f"{self._BASE_URL}/{location}/{date}?key={self._API_KEY}&unitGroup={self.UNIT_GROUP}"

        url = self._append_api_params(url, include, elements)

        response = http_request(url)

        if response is not None:
            try:
                response_json: dict[str, Any] = response.json()
                return response_json
            except (AttributeError, JSONDecodeError):
                logger.error("Weather API returned invalid JSON")

        return None

    # TODO next_x_days is inclusive with today, adapt docstring
    def dynamic_range(
        self,
        location: str,
        dynamic_period: DynamicPeriodEnum,
        include: list[IncludeEnum] | None = None,
        elements: list[ElementsEnum] | None = None,
    ) -> dict[Any, Any] | None:
        """Retrieves dynamic data relative to current date

        Parameters
        ----------
        location : str
            Location format: "city, country" Country needs to be in [Alpha-2](https://www.iban.com/country-codes) Code.
        dynamic_period : DynamicPeriodEnum
            Dynamic Period. Refer to `weather_params.py`.
        elements : list[ElementsEnum] | None, optional
            List of possible properties in a day or hourly data object that should be retrieved from the API. Refer to `weather_params.py`. _By default `None`_.
        include : list[IncludeEnum] | None, optional
            List of possible information that should be retrieved from the API. Refer to `weather_params.py`. _By default `None`_.
        """

        location = location.replace(" ", "")

        if not self._validate_location(location):
            raise Exception("Given location is invalid")

        if not DynamicPeriodEnum.has_value(dynamic_period.value):
            raise Exception("Given DynamicPeriodEnum is invalid")

        # if not self._validate_api_params(include, elements):
        #     raise Exception("Given API params are invalid")

        url = f"{self._BASE_URL}/{location}/{dynamic_period}?key={self._API_KEY}&unitGroup={self.UNIT_GROUP}"

        url = self._append_api_params(url, include, elements)

        response = http_request(url)

        if response is not None:
            try:
                response_json: dict[str, Any] = response.json()
                return response_json
            except (AttributeError, JSONDecodeError):
                logger.error("Weather API returned invalid JSON")

        return None

    def forecast(
        self,
        location: str,
        include: list[IncludeEnum] | None = None,
        elements: list[ElementsEnum] | None = None,
    ) -> dict[Any, Any] | None:
        """Retrieves 15-day weather forecast of given location

        Parameters
        ----------
        location : str
            Location format: "city, country" Country needs to be in [Alpha-2](https://www.iban.com/country-codes) Code.
        elements : list[ElementsEnum] | None, optional
            List of possible properties in a day or hourly data object that should be retrieved from the API. Refer to `weather_params.py`. _By default `None`_.
        include : list[IncludeEnum] | None, optional
            List of possible information that should be retrieved from the API. Refer to `weather_params.py`. _By default `None`_.
        """

        location = location.replace(" ", "")

        if not self._validate_location(location):
            raise Exception("Given location is invalid")

        # if not self._validate_api_params(include, elements):
        #     raise Exception("Given API params are invalid")

        url = f"{self._BASE_URL}/{location}?key={self._API_KEY}&unitGroup={self.UNIT_GROUP}"

        url = self._append_api_params(url, include, elements)

        response = http_request(url)

        if response is not None:
            try:
                response_json: dict[str, Any] = response.json()
                return response_json
            except (AttributeError, JSONDecodeError):
                logger.error("Weather API returned invalid JSON")

        return None
