# ? Disable typing errors for pytest fixtures
# ? Disable private attribute access to test class methods
# pylint: disable=redefined-outer-name,protected-access

import json

import pytest
from currency_converter import CurrencyConverter
from loguru import logger
from loguru._logger import Logger
from pytest_mock import MockFixture
from requests.models import Response

from aswe.api.finance.finance import (
    _get_percentage_change,
    get_currency_by_country,
    get_news_info_by_symbol,
    get_stock_price,
    get_stock_price_change,
    get_stock_rating,
    get_ticker_by_symbol,
)


@pytest.fixture
def http_request_path() -> str:
    """Path for the `http_request` function."""
    return "aswe.api.finance.finance.http_request"


@pytest.fixture
def patch_logger(mocker: MockFixture) -> Logger:
    """Patch the logger."""
    patched_logger: Logger = mocker.patch.object(logger, "error")
    return patched_logger


def test_get_percentage_change() -> None:
    """Test `aswe.api.finance.finance._get_percentage_change`"""
    change = _get_percentage_change("1.23")
    assert change == "+1.23%"

    change = _get_percentage_change("-1.23")
    assert change == "-1.23%"


def test_get_ticker_by_symbol() -> None:
    """Test `aswe.api.finance.finance.get_ticker_by_symbol`"""
    ticker_sentiment = [
        {
            "ticker": "SE",
            "relevance_score": "0.029184",
            "ticker_sentiment_score": "-0.110236",
            "ticker_sentiment_label": "Neutral",
        },
        {
            "ticker": "AAPL",
            "relevance_score": "0.029184",
            "ticker_sentiment_score": "0.066547",
            "ticker_sentiment_label": "Neutral",
        },
        {
            "ticker": "URI",
            "relevance_score": "0.230235",
            "ticker_sentiment_score": "0.181173",
            "ticker_sentiment_label": "Somewhat-Bullish",
        },
        {
            "ticker": "MSFT",
            "relevance_score": "0.173749",
            "ticker_sentiment_score": "0.018912",
            "ticker_sentiment_label": "Neutral",
        },
    ]

    apple_sentiment = get_ticker_by_symbol(ticker_sentiment, "AAPL")
    microsoft_sentiment = get_ticker_by_symbol(ticker_sentiment, "MSFT")

    assert apple_sentiment == {
        "ticker": "AAPL",
        "relevance_score": "0.029184",
        "ticker_sentiment_score": "0.066547",
        "ticker_sentiment_label": "Neutral",
    }

    assert microsoft_sentiment == {
        "ticker": "MSFT",
        "relevance_score": "0.173749",
        "ticker_sentiment_score": "0.018912",
        "ticker_sentiment_label": "Neutral",
    }


def test_get_currency_by_country() -> None:
    """Test `aswe.api.finance.finance.get_currency_by_country`"""
    assert get_currency_by_country("Germany") == ("Euro", "EUR")

    assert get_currency_by_country("United States") == ("US Dollar", "USD")

    assert get_currency_by_country("Christmas Island") == ("Australian Dollar", "AUD")


def test_get_currency_by_country_invalid_country() -> None:
    """Test `aswe.api.finance.finance.get_currency_by_country` with invalid country."""
    assert get_currency_by_country("Deutschland GmbH") == ("US Dollar", "USD")


def test_get_news_info_by_symbol(mocker: MockFixture, http_request_path: str) -> None:
    """Test `aswe.api.finance.finance.get_news_info_by_symbol`"""
    mock_valid_response_object = {
        "items": "50",
        "sentiment_score_definition": "x <= -0.35: Bearish; -0.35 < x <= -0.15: Somewhat-Bearish; -0.15 < x < 0.15: Neutral; 0.15 <= x < 0.35: Somewhat_Bullish; x >= 0.35: Bullish",
        "relevance_score_definition": "0 < x <= 1, with a higher score indicating higher relevance.",
        "feed": [
            {
                "title": "Title 1",
                "url": "...",
                "time_published": "20221206T161745",
                "authors": ["Benzinga Gaming"],
                "summary": "Summary 1",
                "banner_image": "...",
                "source": "Benzinga",
                "category_within_source": "General",
                "source_domain": "www.benzinga.com",
                "topics": [
                    {"topic": "Financial Markets", "relevance_score": "0.538269"},
                ],
                "overall_sentiment_score": 0.064738,
                "overall_sentiment_label": "Neutral",
                "ticker_sentiment": [
                    {
                        "ticker": "MSFT",
                        "relevance_score": "0.050733",
                        "ticker_sentiment_score": "0.105365",
                        "ticker_sentiment_label": "Neutral",
                    },
                    {
                        "ticker": "AAPL",
                        "relevance_score": "0.225367",
                        "ticker_sentiment_score": "0.052527",
                        "ticker_sentiment_label": "Neutral",
                    },
                ],
            },
            {
                "title": "Title 2",
                "url": "...",
                "time_published": "20221206T161745",
                "authors": ["Benzinga Gaming"],
                "summary": "Summary 2",
                "banner_image": "...",
                "source": "Benzinga",
                "category_within_source": "General",
                "source_domain": "www.benzinga.com",
                "topics": [
                    {"topic": "Financial Markets", "relevance_score": "0.538269"},
                ],
                "overall_sentiment_score": 0.064738,
                "overall_sentiment_label": "Neutral",
                "ticker_sentiment": [
                    {
                        "ticker": "MSFT",
                        "relevance_score": "0.95",
                        "ticker_sentiment_score": "0.105365",
                        "ticker_sentiment_label": "Neutral",
                    },
                    {
                        "ticker": "AAPL",
                        "relevance_score": "0.225367",
                        "ticker_sentiment_score": "0.052527",
                        "ticker_sentiment_label": "Neutral",
                    },
                ],
            },
            {
                "title": "Title 3",
                "url": "...",
                "time_published": "20221206T161745",
                "authors": ["Benzinga Gaming"],
                "summary": "Summary 3",
                "banner_image": "...",
                "source": "Benzinga",
                "category_within_source": "General",
                "source_domain": "www.benzinga.com",
                "topics": [
                    {"topic": "Financial Markets", "relevance_score": "0.538269"},
                ],
                "overall_sentiment_score": 0.064738,
                "overall_sentiment_label": "Neutral",
                "ticker_sentiment": [
                    {
                        "ticker": "MSFT",
                        "relevance_score": "0.850733",
                        "ticker_sentiment_score": "0.105365",
                        "ticker_sentiment_label": "Neutral",
                    },
                    {
                        "ticker": "AAPL",
                        "relevance_score": "0.225367",
                        "ticker_sentiment_score": "0.052527",
                        "ticker_sentiment_label": "Neutral",
                    },
                ],
            },
            {
                "title": "Title 4",
                "url": "...",
                "time_published": "20221206T161745",
                "authors": ["Benzinga Gaming"],
                "summary": "Summary 4",
                "banner_image": "...",
                "source": "Benzinga",
                "category_within_source": "General",
                "source_domain": "www.benzinga.com",
                "topics": [
                    {"topic": "Financial Markets", "relevance_score": "0.538269"},
                ],
                "overall_sentiment_score": 0.064738,
                "overall_sentiment_label": "Neutral",
                "ticker_sentiment": [
                    {
                        "ticker": "MSFT",
                        "relevance_score": "0.98733",
                        "ticker_sentiment_score": "0.105365",
                        "ticker_sentiment_label": "Neutral",
                    },
                    {
                        "ticker": "AAPL",
                        "relevance_score": "0.225367",
                        "ticker_sentiment_score": "0.052527",
                        "ticker_sentiment_label": "Neutral",
                    },
                ],
            },
        ],
    }

    valid_response = Response()
    valid_response._content = json.dumps(mock_valid_response_object).encode()
    mocker.patch(http_request_path, return_value=valid_response)

    apple_news = get_news_info_by_symbol("MSFT")

    assert isinstance(apple_news, list)
    assert len(apple_news) > 0 and len(apple_news) <= 3
    assert all(isinstance(news, dict) for news in apple_news)
    assert all(all(key in news for key in ["title", "authors", "source", "ticker_sentiment"]) for news in apple_news)


def test_get_news_info_by_symbol_invalid_response(mocker: MockFixture, http_request_path: str) -> None:
    """Test `aswe.api.finance.finance.get_news_info_by_symbol` with invalid response."""
    mocker.patch(http_request_path, return_value=None)

    apple_news = get_news_info_by_symbol("AAPl")

    assert apple_news is None

    invalid_response_object = {"fied": "articles"}
    invalid_response = Response()
    invalid_response._content = json.dumps(invalid_response_object).encode()
    mocker.patch(http_request_path, return_value=invalid_response)
    spy_logger_error = mocker.spy(logger, "error")

    apple_news = get_news_info_by_symbol("AAPL")
    spy_logger_error.assert_called_once_with("Got invalid response from News Sentiment API.")


def test_get_stock_price(mocker: MockFixture, http_request_path: str) -> None:
    """Test `aswe.api.finance.finance.get_stock_price`"""
    mock_valid_response_object = [{"symbol": "AAPL", "price": 120.96000000, "volume": 332607163}]
    valid_response = Response()
    valid_response._content = json.dumps(mock_valid_response_object).encode()
    mocker.patch(http_request_path, return_value=valid_response)

    apple_price = get_stock_price("AAPL")

    assert isinstance(apple_price, float)
    assert apple_price == 120.96


def test_get_stock_price_other_currency(mocker: MockFixture, http_request_path: str) -> None:
    """Test `aswe.api.finance.finance.get_stock_price` with currency conversion."""
    cur_conv = CurrencyConverter()

    mock_valid_response_object = [{"symbol": "AAPL", "price": 120.96000000, "volume": 332607163}]
    valid_response = Response()
    valid_response._content = json.dumps(mock_valid_response_object).encode()
    mocker.patch(http_request_path, return_value=valid_response)

    apple_price = get_stock_price("AAPL", "EUR")

    assert isinstance(apple_price, float)
    assert apple_price == round(cur_conv.convert(120.96, "USD", "EUR"), 2)


def test_get_stock_price_invalid_response(mocker: MockFixture, http_request_path: str) -> None:
    """Test `aswe.api.finance.finance.get_stock_price` with invalid response."""
    mocker.patch(http_request_path, return_value=None)

    apple_price = get_stock_price("AAPL")
    assert apple_price is None

    invalid_response_object = [{"symbol": "AAPL", "preis": 120.96000000, "volume": 332607163}]
    invalid_response = Response()
    invalid_response._content = json.dumps(invalid_response_object).encode()
    mocker.patch(http_request_path, return_value=invalid_response)
    spy_logger_error = mocker.spy(logger, "error")

    apple_price = get_stock_price("AAPL")
    spy_logger_error.assert_called_once_with("Got invalid response from Stock API.")

    invalid_response_object = []
    valid_response = Response()
    valid_response._content = json.dumps(invalid_response_object).encode()
    mocker.patch(http_request_path, return_value=valid_response)
    spy_logger_error = mocker.spy(logger, "error")

    apple_price = get_stock_price("AAPL")
    spy_logger_error.assert_called_once_with("Could not find stock price for symbol: AAPL.")


def test_get_stock_price_change(mocker: MockFixture, http_request_path: str) -> None:
    """Test `aswe.api.finance.finance.get_stock_price_change`"""

    mock_valid_response_object = [
        {
            "symbol": "AAPL",
            "1D": -1.92,
            "5D": 3.86,
            "1M": -11.55,
            "3M": -10.6,
            "6M": -11.34,
            "ytd": -21.37,
            "1Y": 14.1,
            "3Y": 218.62,
            "5Y": 272.2,
            "10Y": 602.31,
            "max": 111401.54,
        }
    ]
    valid_response = Response()
    valid_response._content = json.dumps(mock_valid_response_object).encode()
    mocker.patch(http_request_path, return_value=valid_response)

    apple_price_change = get_stock_price_change("AAPL")

    assert apple_price_change == {
        "24h": "-1.92%",
        "5D": "+3.86%",
    }


def test_get_stock_price_change_invalid_response(mocker: MockFixture, http_request_path: str) -> None:
    """Test `aswe.api.finance.finance.get_stock_price_change` with inval"""
    mocker.patch(http_request_path, return_value=None)

    apple_price_change = get_stock_price_change("AAPL")

    assert apple_price_change is None

    invalid_response_object = [
        {
            "symbol": "AAPL",
            "einsDeh": -1.92,
            "5D": 3.86,
            "1M": -11.55,
            "3M": -10.6,
            "6M": -11.34,
            "ytd": -21.37,
            "1Y": 14.1,
            "3Y": 218.62,
            "5Y": 272.2,
            "10Y": 602.31,
            "max": 111401.54,
        }
    ]
    invalid_response = Response()
    invalid_response._content = json.dumps(invalid_response_object).encode()
    mocker.patch(http_request_path, return_value=invalid_response)
    spy_logger_error = mocker.spy(logger, "error")

    apple_price_change = get_stock_price_change("AAPL")
    spy_logger_error.assert_called_once_with("Got invalid response from Stock API.")

    invalid_response_object = []
    invalid_response = Response()
    invalid_response._content = json.dumps(invalid_response_object).encode()
    mocker.patch(http_request_path, return_value=invalid_response)
    spy_logger_error = mocker.spy(logger, "error")

    apple_price_change = get_stock_price_change("AAPL")
    spy_logger_error.assert_called_once_with("Could not find stock price change for symbol: AAPL.")


def test_get_stock_rating(mocker: MockFixture, http_request_path: str) -> None:
    """Test `aswe.api.finance.finance.get_stock_rating`"""
    mock_valid_response_object = [
        {
            "symbol": "AAPL",
            "date": "2020-09-04",
            "rating": "S-",
            "ratingScore": 5,
            "ratingRecommendation": "Strong Buy",
            "ratingDetailsDCFScore": 5,
            "ratingDetailsDCFRecommendation": "Strong Buy",
            "ratingDetailsROEScore": 4,
            "ratingDetailsROERecommendation": "Buy",
            "ratingDetailsROAScore": 3,
            "ratingDetailsROARecommendation": "Neutral",
            "ratingDetailsDEScore": 5,
            "ratingDetailsDERecommendation": "Strong Buy",
            "ratingDetailsPEScore": 5,
            "ratingDetailsPERecommendation": "Strong Buy",
            "ratingDetailsPBScore": 5,
            "ratingDetailsPBRecommendation": "Strong Buy",
        }
    ]
    valid_response = Response()
    valid_response._content = json.dumps(mock_valid_response_object).encode()
    mocker.patch(http_request_path, return_value=valid_response)

    apple_rating = get_stock_rating("AAPL")

    assert apple_rating == "S minus (Strong Buy)"


def test_get_stock_rating_invalid_response(mocker: MockFixture, http_request_path: str) -> None:
    """Test `aswe.api.finance.finance.get_stock_rating` with invalid response."""
    mocker.patch(http_request_path, return_value=None)

    apple_rating = get_stock_rating("AAPL")
    assert apple_rating is None

    invalid_response_object = [
        {
            "symbol": "AAPL",
            "date": "2020-09-04",
            "raaatting": "S-",
            "ratingScore": 5,
            "ratingRecommendation": "Strong Buy",
            "ratingDetailsDCFScore": 5,
            "ratingDetailsDCFRecommendation": "Strong Buy",
            "ratingDetailsROEScore": 4,
            "ratingDetailsROERecommendation": "Buy",
            "ratingDetailsROAScore": 3,
            "ratingDetailsROARecommendation": "Neutral",
            "ratingDetailsDEScore": 5,
            "ratingDetailsDERecommendation": "Strong Buy",
            "ratingDetailsPEScore": 5,
            "ratingDetailsPERecommendation": "Strong Buy",
            "ratingDetailsPBScore": 5,
            "ratingDetailsPBRecommendation": "Strong Buy",
        }
    ]
    invalid_response = Response()
    invalid_response._content = json.dumps(invalid_response_object).encode()
    mocker.patch(http_request_path, return_value=invalid_response)
    spy_logger_error = mocker.spy(logger, "error")

    apple_rating = get_stock_rating("AAPL")
    spy_logger_error.assert_called_once_with("Got invalid response from Stock API.")

    invalid_response_object = []
    invalid_response = Response()
    invalid_response._content = json.dumps(invalid_response_object).encode()
    mocker.patch(http_request_path, return_value=invalid_response)
    spy_logger_error = mocker.spy(logger, "error")

    apple_rating = get_stock_rating("AAPL")
    spy_logger_error.assert_called_once_with("Could not find stock rating for symbol: AAPL.")
