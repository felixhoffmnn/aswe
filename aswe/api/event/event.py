import os
from typing import Final


class EventApi:
    """Crawler Class retrieves data from
    [ticketmaster](https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/)"""

    _BASE_URL: Final[str] = "https://app.ticketmaster.com/discovery/v2/"
    _API_KEY: Final[str] = os.getenv("EVENT_API_KEY", "")

    def __init__(self) -> None:
        self._validate_api_key()

    def _validate_api_key(self) -> None:
        if self._API_KEY == "":
            raise Exception("EVENT_API_KEY was not loaded into system")

    def events(self) -> str:
        # TODO fix return type

        url = f"{self._BASE_URL}/events?apikey={self._API_KEY}"

        return url

        # response = http_request(url)
        # try:
        #     response_json = dict(response.json())

        #     return response_json
        # except JSONDecodeError as err:
        #     logger.error(f"Event API returned invalid JSON: {err}")
        # except Exception as err:
        #     logger.error(f"Something went wrong: {err}")
