import os

from dotenv import load_dotenv

from aswe.utils.request import http_request

load_dotenv()

API_key = os.getenv("NEWS_API_KEY")


def top_headlines_search(country: str = "us", max_results: int = 3) -> list[str] | None:
    """_summary_

    Parameters
    ----------
    country : str, optional
        Name of the country the news will be about, by default "us"
    max_results : int, optional
        Number of news article returned, by default 3

    Returns
    -------
    list[str] | None
        Return a list of strings with the news articles
    """
    result = []
    request = http_request(f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={API_key}")
    if request is None:
        return None
    headline_request = request.json()
    if max_results > len(headline_request["articles"]):
        max_results = len(headline_request["articles"])
    for i in range(max_results):
        result.append(headline_request["articles"][i]["title"] + ": " + headline_request["articles"][i]["description"])
    return result


def keyword_search(keyword: str, max_results: int = 3) -> list[str] | None:
    """_summary_

    Parameters
    ----------
    keyword : str
        Keyword which the news will be about
    max_results : int, optional
        Number of news articles that will be returned, by default 3

    Returns
    -------
    list[str] | None
        Return a list of strings with the news articles
    """
    result = []
    request = http_request(f"https://newsapi.org/v2/everything?q={keyword}&apiKey={API_key}")
    if request is None:
        return None
    keyword_request = request.json()
    if max_results > len(keyword_request["articles"]):
        max_results = len(keyword_request["articles"])
    for i in range(max_results):
        result.append(keyword_request["articles"][i]["title"] + ": " + keyword_request["articles"][i]["description"])
    return result
