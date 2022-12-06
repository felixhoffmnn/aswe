from datetime import datetime

from loguru import logger
from requests import Response


def validate_date(date: str, include_time: bool | None = None) -> bool:
    """Validates Time format for either `YYYY-MM-DD` or `YYYY-MM-DDThh:mm:ss`

    * TODO: Check if format is correct (`YYYY-MM-DDThh:mm:ss` or `YYYY-MM-DDThh:mm:ssZ`)

    Parameters
    ----------
    date : str
        Date as type string that should be checked
    include_time : bool | None, optional
        Whether date should include time. If None methods tries finding correct type. _By default `None`._

    Returns
    -------
    bool:
        Whether date is valid.
    """
    if ("T" in date and include_time is None) or include_time is True:
        try:
            datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            logger.error(f"Incorrect date format, required: `YYYY-MM-DDThh:mm:ssZ`, given: {date}")
            return False
    else:
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            logger.error(f"Incorrect date format, required: `YYYY-MM-DD`, given: {date}")
            return False

    return True


def validate_api_limit_reached(response: Response) -> bool:
    """Test if the API limit is reached

    Parameters
    ----------
    response : Response
        Response of the API request

    Returns
    -------
    bool
        True if the API limit is reached
    """
    try:
        if "You have reached the request limit for the day" in response.json()["errors"]["requests"]:
            return True
    except KeyError:
        return False
    except TypeError:
        return False

    return False
