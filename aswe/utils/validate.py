from datetime import datetime

from loguru import logger


def validate_date(date: str) -> bool:
    """Validates Time format for either `YYYY-MM-DD` or `YYYY-MM-DDThh:mm:ss`

    Parameters
    ----------
    date : str
        Date as type string that should be checked

    Returns
    -------
    bool:
        Whether date is valid.
    """
    if "T" in date:
        try:
            datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            logger.error(f"Incorrect date format, required: `YYYY-MM-DDThh:mm:ss`, given: {date}")
            return False
    else:
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            logger.error(f"Incorrect date format, required: YYYY-MM-DD, given: {date}")
            return False

    return True
