from datetime import datetime

from loguru import logger


def validate_date(date: str, include_time: bool | None = None) -> bool:
    """Validates Time format for either `YYYY-MM-DD` or `YYYY-MM-DDThh:mm:ss`

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
