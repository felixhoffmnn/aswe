from typing import Optional
import requests
from loguru import logger
from typing import Optional


def http_request(url: str, headers: dict = {}, timeout: int = 10) -> Optional[str]:
    """Send a HTTP request to the given URL and return the response.

    Args:
        url (str): The URL of the API.
        timeout (int, optional): The time in seconds to wait for a response. Defaults to 10.

    Returns:
        Optional[str]: The response from the API or None if the request failed.
    """
    try:
        response = requests.get(url, timeout=timeout, headers=headers)
        response.raise_for_status()
    except requests.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logger.error(f"Other error occurred: {err}")
    else:
        print("Success!")
        return response.json()
