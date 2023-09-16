from typing import Callable, Optional
from datetime import date
from newsapi import NewsApiClient, newsapi_exception
from ....db.base import Digest
from .content import NewsContent
from .utils import merge_meta_and_text
from theroast.config import api_config

MAX_TRIES = 3
EXCLUDE_DOMAINS = "google.com"
LANGUAGE = "en"

class NewsSource():
    def __init__(self):
        """
        Source object with default methods for Getting Data.
        """
        if not api_config.NEWS_API_KEY: raise ValueError("NEWS_API_KEY not set")
        self.cli: NewsApiClient = NewsApiClient(api_config.NEWS_API_KEY)
        self.content: NewsContent = NewsContent()

    def _get_newsapi(self, digest: dict, method: Callable, **kwargs):
        interests = " OR ".join(digest["interests"])
        # sources = ",".join(digest["sources"])
        sources = None
        for _ in range(MAX_TRIES):
            try:
                return method(q=interests, sources=sources, **kwargs)
            except newsapi_exception.NewsAPIException as error:
                print(error)
        return None

    def get_sources(self, language: Optional[str]=LANGUAGE, **kwargs):
        if not self.cli: raise ValueError("NewsApiClient not initialized")
        return self.cli.get_sources(language=language, **kwargs)

    def get_all(self, digest: dict):
        today = date.today()
        _data = self._get_newsapi(
            digest,
            self.cli.get_everything,
            from_param=f"{today.year:04}-{today.month:02}-{(today.day-2):02}",
            exclude_domains=EXCLUDE_DOMAINS
        )
        urls = [article["url"] for article in _data["articles"]]
        articles = self.content.get_content(urls)
        data = merge_meta_and_text(_data["articles"], articles)
        return data

    def get_top(self, digest: dict):
        _data = self._get_newsapi(
            digest,
            self.cli.get_top_headlines,
            country="us"
        )
        print(_data)
        urls = [article["url"] for article in _data["articles"]]
        print(urls)
        articles = self.content.get_content(urls)
        return articles