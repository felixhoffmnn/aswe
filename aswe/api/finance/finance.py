import os
from datetime import datetime, timedelta
from json import JSONDecodeError
from pathlib import Path
from typing import Any, Final

import pandas as pd
from currency_converter import CurrencyConverter
from loguru import logger

from aswe.utils.request import http_request

_FMP_BASE_URL: Final[str] = "https://financialmodelingprep.com/api/v3"
_AV_BASE_URL: Final[str] = "https://www.alphavantage.co"

_FMP_API_KEY: Final[str] = os.getenv("FINANCE_API_KEY_1", "")
_AV_API_KEY: Final[str] = os.getenv("FINANCE_API_KEY_2", "")

_CC_MAPPING_PATH: Final[str] = "data/finance/country_currency_mapping.csv"

cur_conv = CurrencyConverter()


# Stock price data


def get_currency_by_country(country: str) -> tuple[str, str]:
    """Returns the currency and the currency symbol for a given country.

    Parameters
    ----------
    country : str
        The country for which the currency should be returned.

    Returns
    -------
    Tuple[str, str]
        A tuple containing the currency and the currency symbol.
    """ """"""
    with open(Path(_CC_MAPPING_PATH), encoding="utf-8") as mapping_file:
        country_currency_mapping = pd.read_csv(mapping_file)
    try:
        given_country_data = country_currency_mapping[country_currency_mapping["ENTITY"] == country.upper()].iloc[0]
        return (given_country_data["Currency"], given_country_data["Alphabetic Code"])
    except IndexError:
        logger.warning(f"Could not find currency for country: {country}. Using USD instead.")
    return ("US Dollar", "USD")


def get_stock_price(symbol: str, currency: str = "USD") -> float | None:
    """Returns the current stock price for a given symbol.

    Parameters
    ----------
    symbol : str
        The symbol for which the stock price should be returned.
    currency : str, optional
        The currency in which the stock price should be returned, by default "USD"

    Returns
    -------
    float | None
        The current stock price for the given symbol.
    """
    response = http_request(f"{_FMP_BASE_URL}/quote-short/{symbol}?apikey={_FMP_API_KEY}")
    if response is not None:
        try:
            price = response.json()[0]["price"]
            if currency != "USD":
                price = cur_conv.convert(price, "USD", currency)
            return float(round(price, 2))
        except (AttributeError, JSONDecodeError):
            logger.error("Got invalid response from Stock API.")
        except IndexError:
            logger.warning(f"Could not find stock price for symbol: {symbol}.")
    return None


def get_stock_rating(symbol: str) -> str | None:
    """Returns the current stock rating for a given symbol.

    Parameters
    ----------
    symbol : str
        The symbol for which the stock rating should be returned.

    Returns
    -------
    str | None
        The current stock rating for the given symbol.
    """
    response = http_request(f"{_FMP_BASE_URL}/rating/{symbol}?apikey={_FMP_API_KEY}")
    if response is not None:
        try:
            rating_data = response.json()[0]
            rating = f"{rating_data['rating']} ({rating_data['ratingRecommendation']})"
            return rating
        except (AttributeError, JSONDecodeError):
            logger.error("Got invalid response from Stock API.")
        except IndexError:
            logger.warning(f"Could not find stock rating for symbol: {symbol}.")
    return None


def _get_percentage_change(change: str) -> str:
    """Returns a formatted percentage change string.

    Parameters
    ----------
    change : str
        The percentage change as a string.

    Returns
    -------
    str
        The formatted percentage change string.
    """
    if float(change) > 0:
        return f"+{change}%"
    else:
        return f"{change}%"


def get_stock_price_change(symbol: str) -> dict[str, str] | None:
    """Returns the current stock price change for a given symbol.

    Parameters
    ----------
    symbol : str
        The symbol for which the stock price change should be returned.

    Returns
    -------
    dict[str, str] | None
        The current stock price change (per day and per 5 days) for the given symbol.
    """
    response = http_request(f"{_FMP_BASE_URL}/stock-price-change/{symbol}?apikey={_FMP_API_KEY}")
    if response is not None:
        try:
            change_data = response.json()[0]
            change = {
                "24h": _get_percentage_change(change_data["1D"]),
                "5D": _get_percentage_change(change_data["5D"]),
            }
            return change
        except (AttributeError, JSONDecodeError):
            logger.error("Got invalid response from Stock API.")
        except IndexError:
            logger.error(f"Could not find stock price change for symbol: {symbol}.")
    return None


# Financial news sentiment


def get_news_info_by_symbol(symbol: str) -> list[dict[str, Any]] | None:
    """Returns the latest news for a given symbol.

    Parameters
    ----------
    symbol : str
        The symbol for which the latest news should be returned.

    Returns
    -------
    list[list[dict[str, str]]] | None
        The three most relevant news in the last 24h for the given symbol.
    """
    one_day_ago = (datetime.utcnow() - timedelta(days=1)).strftime("%Y%m%dT%H%M")
    response = http_request(
        f"""{_AV_BASE_URL}/query?function=NEWS_SENTIMENT&tickers={symbol}&time_from="""
        f"""{one_day_ago}&sort=latest&limit=200&apikey={_AV_API_KEY}"""
    )
    if response is not None:
        try:
            all_news = response.json()["feed"]
            most_relevant_news = list(
                filter(
                    lambda news: float(_get_ticker_by_symbol(news["ticker_sentiment"], symbol)["relevance_score"])
                    >= 0.8,
                    all_news,
                )
            )[:3]
            return most_relevant_news
        except (AttributeError, JSONDecodeError):
            logger.error("Got invalid response from News Sentiment API.")
    return None


def _get_ticker_by_symbol(ticker_list: list[dict[str, str]], symbol: str) -> dict[str, str]:
    """Returns the ticker data for a given symbol.

    Parameters
    ----------
    ticker_list : list[dict[str, str]]
        The list of ticker data from a news source.
    symbol : str
        The symbol for which the ticker data should be returned.

    Returns
    -------
    dict[str, str]
        The ticker data for the given symbol.
    """
    return next(ticker for ticker in ticker_list if ticker["ticker"] == symbol)
