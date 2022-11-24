import os
from typing import Any, Final

from loguru import logger
from requests import JSONDecodeError

from aswe.api.event.event_params import (
    EventApiClassificationParams,
    EventApiEventParams,
)
from aswe.utils.request import http_request


class EventApi:
    """Crawler Class retrieves data from
    [ticketmaster](https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/)

    * TODO: Add Attributes section
    """

    _BASE_URL: Final[str] = "https://app.ticketmaster.com/discovery/v2/"
    _API_KEY: Final[str] = os.getenv("EVENT_API_KEY", "")

    def __init__(self) -> None:
        self._validate_api_key()

    def _validate_api_key(self) -> None:
        if self._API_KEY == "":
            raise Exception("EVENT_API_KEY was not loaded into system")

    def events(self, query_params: EventApiEventParams) -> dict[Any, Any] | None:
        """Retrieves Events that fulfil given query parameters

        Args:
            query_params (`EventApiEventParams`): Query Parameters API should filter for.
        """
        if not query_params.validate_fields():
            raise Exception("Given Event Api Event Params are invalid.")

        url = f"{self._BASE_URL}events?apikey={self._API_KEY}&{query_params.concat_to_query()}"

        response = http_request(url)

        if response:
            try:
                response_json = dict(response.json())
                return response_json
            except JSONDecodeError as err:
                logger.error(f"Event API returned invalid Json: {err}")
            except Exception as err:
                logger.error(f"Something went wrong: {err}")

        return None

    def classifications(self, query_params: EventApiClassificationParams) -> dict[Any, Any] | None:
        """Retrieves Classifications that fulfil given query parameters.

        Args:
            query_params (`EventApiClassificationParams`): Query Parameters API should filter for.
        """
        if not query_params.validate_fields():
            raise Exception("Given Event Api Classification Params are invalid.")

        url = f"{self._BASE_URL}classifications?apikey={self._API_KEY}&{query_params.concat_to_query()}"

        response = http_request(url)

        if response:
            try:
                response_json = dict(response.json())
                return response_json
            except JSONDecodeError as err:
                logger.error(f"Event API returned invalid Json: {err}")
            except Exception as err:
                logger.error(f"Something went wrong: {err}")

        return None
