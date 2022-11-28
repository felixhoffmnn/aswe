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

    def _reduce_events(self, events: dict[Any, Any]) -> list[dict[Any, Any]]:
        if "_embedded" in events:
            reduced_events = []

            for event in events["_embedded"]["events"]:
                # ? remove if too few event can be found ----------------------
                # ! skip offsale or cancelled events --------------------------
                if event["dates"]["status"]["code"] in ["offsale", "cancelled"]:
                    continue
                # ! -----------------------------------------------------------

                try:
                    single_event = {
                        "id": event["id"],
                        "name": event["name"],
                        "start": event["dates"]["start"]["dateTime"],
                        "status": event["dates"]["status"]["code"],
                        "location": {
                            "name": event["_embedded"]["venues"][0]["name"],
                            "city": event["_embedded"]["venues"][0]["city"]["name"],
                            "address": event["_embedded"]["venues"][0]["address"],
                        },
                    }

                    reduced_events.append(single_event)
                except Exception as err:
                    logger.error(err)
            return reduced_events

        return []

    def events(self, query_params: EventApiEventParams) -> list[dict[Any, Any]] | None:
        """Retrieves Events that fulfil given query parameters

        Parameters
        ----------
        query_params : EventApiEventParams
            Query Parameters API should filter for.

        Returns
        -------
        list[dict[Any, Any]] | None
            List of events

        """

        if not query_params.validate_fields():
            raise Exception("Given Event Api Event Params are invalid.")

        url = f"{self._BASE_URL}events?apikey={self._API_KEY}&{query_params.concat_to_query()}"

        response = http_request(url)

        if response:
            try:
                response_json = dict(response.json())
                reduced_events = self._reduce_events(response_json)

                return reduced_events
            except JSONDecodeError as err:
                logger.error(f"Event API returned invalid Json: {err}")
            except Exception as err:
                logger.error(f"Something went wrong: {err}")

        return None

    def classifications(self, query_params: EventApiClassificationParams) -> dict[Any, Any] | None:
        """Retrieves Classifications that fulfil given query parameters.

        Parameters
        ----------
        query_params : EventApiClassificationParams
            Query Parameters API should filter for.

        Returns
        -------
        dict[Any, Any] | None
            Dictionary of classifications
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
