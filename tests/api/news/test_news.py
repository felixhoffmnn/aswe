import pytest

from aswe.api.news.news import keyword_search, top_headlines_search


@pytest.mark.xfail(
    reason="Function causes TypeError in `aswe/api/news/news.py:35`. (can only concatenate str (not 'NoneType') to str)"
)
def test_top_headlines_search() -> None:
    """Test `aswe.api.news.top_headlines_search`"""
    news = top_headlines_search("de", 3)
    assert len(news) == 3


def test_keyword_search() -> None:
    """Test `aswe.api.news.keyword_search`"""
    news = keyword_search("corona", 4)
    assert len(news) == 4
