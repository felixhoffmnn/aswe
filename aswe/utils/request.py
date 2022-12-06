from typing import Any

import requests
from loguru import logger
from requests import HTTPError, Response

from aswe.utils.error import TooManyRequests


def http_request(url: str, headers: dict[Any, Any] | None = None, timeout: int = 10) -> Response | None:
    """Send a HTTP request to the given URL and return the response.

    Parameters
    ----------
    url : str
        The URL of the API.
    headers : dict[Any, Any] | None, optional
        The headers to send with the request. _By default `None`._
    timeout : int, optional
        The time in seconds to wait for a response. _By default `10`.

    Returns
    -------
    Response | None
        The response from the API or None if the request failed.
    """
    try:
        response = requests.get(url, timeout=timeout, headers=headers)

        response.raise_for_status()
        if not response.status_code == 200:
            raise Exception("HTTP status code is not 200")
    except HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        if http_err.response.status_code == 429 or http_err.response.status_code == 403:
            raise TooManyRequests from http_err
        return None
    except Exception as err:
        logger.error(f"Other error occurred: {err}")
        return None

    logger.success(f"Successfully fetched data from {url} with status code {response.status_code}")
    return response
