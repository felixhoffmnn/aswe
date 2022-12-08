import os

from aswe.utils.request import http_request

_NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def top_headlines_search(country: str = "us", max_results: int = 3) -> list[str] | None:
    """Get the top headlines of a country

    Parameters
    ----------
    country : str, optional
        Name of the country the news will be about. _By default `us`._
    max_results : int, optional
        Number of news article returned. _By default `3`._

    Returns
    -------
    list[str] | None
        Return a list of strings with the news articles
    """
    result = []
    request = http_request(f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={_NEWS_API_KEY}")
    if request is None:
        return None
    headline_request = request.json()
    if max_results > len(headline_request["articles"]):
        max_results = len(headline_request["articles"])
    for i in range(max_results):
        if headline_request["articles"][i]["description"] is None:
            result.append(headline_request["articles"][i]["title"])
        else:
            result.append(
                headline_request["articles"][i]["title"] + ": " + headline_request["articles"][i]["description"]
            )
    return result


def keyword_search(keyword: str, max_results: int = 3) -> list[str] | None:
    """Get the top headlines for a keyword

    Parameters
    ----------
    keyword : str
        Keyword which the news will be about
    max_results : int, optional
        Number of news articles that will be returned. _By default `3`._

    Returns
    -------
    list[str] | None
        Return a list of strings with the news articles
    """
    result = []
    request = http_request(f"https://newsapi.org/v2/everything?q={keyword}&apiKey={_NEWS_API_KEY}")
    if request is None:
        return None
    keyword_request = request.json()
    if max_results > len(keyword_request["articles"]):
        max_results = len(keyword_request["articles"])
    for i in range(max_results):
        result.append(keyword_request["articles"][i]["title"] + ": " + keyword_request["articles"][i]["description"])
    return result
