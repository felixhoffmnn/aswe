import pytest

from aswe.api.finance.finance import (
    _get_percentage_change,
    _get_ticker_by_symbol,
    get_currency_by_country,
    get_news_info_by_symbol,
    get_stock_price,
    get_stock_price_change,
    get_stock_rating,
)
from aswe.utils.error import TooManyRequests


def test_get_percentage_change() -> None:
    """Test `aswe.api.finance.finance._get_percentage_change`"""
    change = _get_percentage_change("1.23")
    assert change == "+1.23%"

    change = _get_percentage_change("-1.23")
    assert change == "-1.23%"


@pytest.mark.xfail(raises=TooManyRequests)
def test_get_ticker_by_symbol() -> None:
    """Test `aswe.api.finance.finance._get_ticker_by_symbol`"""
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

    apple_sentiment = _get_ticker_by_symbol(ticker_sentiment, "AAPL")
    microsoft_sentiment = _get_ticker_by_symbol(ticker_sentiment, "MSFT")

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

    assert get_currency_by_country("Deutschland GmbH") == ("US Dollar", "USD")


@pytest.mark.xfail(raises=TooManyRequests)
def test_get_news_info_by_symbol() -> None:
    """Test `aswe.api.finance.finance.get_news_info_by_symbol`"""
    apple_news = get_news_info_by_symbol("AAPL")

    assert isinstance(apple_news, list)
    assert len(apple_news) > 0 and len(apple_news) <= 3
    assert all(isinstance(news, dict) for news in apple_news)
    assert all(all(key in news for key in ["title", "authors", "source", "ticker_sentiment"]) for news in apple_news)


@pytest.mark.xfail(raises=TooManyRequests)
def test_get_stock_price() -> None:
    """Test `aswe.api.finance.finance.get_stock_price`"""
    apple_price = get_stock_price("AAPL")
    microsoft_price = get_stock_price("MSFT")
    microsoft_price_euro = get_stock_price("MSFT", "EUR")
    unknown_price = get_stock_price("UNKNOWN")

    assert isinstance(apple_price, float)

    assert isinstance(microsoft_price, float)

    assert isinstance(microsoft_price_euro, float)

    assert unknown_price is None


@pytest.mark.xfail(raises=TooManyRequests)
def test_get_stock_price_change() -> None:
    """Test `aswe.api.finance.finance.get_stock_price_change`"""
    apple_price_change = get_stock_price_change("AAPL")
    microsoft_price_change = get_stock_price_change("MSFT")
    unknown_price_change = get_stock_price_change("UNKNOWN")

    assert isinstance(apple_price_change, dict)
    assert all(key in apple_price_change for key in ["24h", "5D"])
    assert all(isinstance(value, str) for value in apple_price_change.values())

    assert isinstance(microsoft_price_change, dict)
    assert all(key in microsoft_price_change for key in ["24h", "5D"])
    assert all(isinstance(value, str) for value in microsoft_price_change.values())

    assert unknown_price_change is None


@pytest.mark.xfail(raises=TooManyRequests)
def test_get_stock_rating() -> None:
    """Test `aswe.api.finance.finance.get_stock_rating`"""
    apple_rating = get_stock_rating("AAPL")
    microsoft_rating = get_stock_rating("MSFT")
    unknown_rating = get_stock_rating("UNKNOWN")

    assert isinstance(apple_rating, str)

    assert isinstance(microsoft_rating, str)

    assert unknown_rating is None
