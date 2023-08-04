from typing import Callable, Optional
from datetime import date
from newsapi import NewsApiClient, newsapi_exception
from ....db.base import Digest
from .content import NewsContent
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

    def _get_newsapi(self, digest: Digest, method: Callable, **kwargs):
        if not self.cli: raise ValueError("NewsApiClient not initialized")
        if not digest.interests: raise ValueError("Interests not specified")
        interests = " OR ".join(digest.interests)
        # sources = ",".join(digest.sources)
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

    def get_all(self, digest: Digest):
        if not digest: raise ValueError("Digest not specified")
        today = date.today()
        _data = self._get_newsapi(
            digest,
            self.cli.get_everything,
            from_param=f"{today.year:04}-{today.month:02}-{(today.day-2):02}",
            exclude_domains=EXCLUDE_DOMAINS
        )
        urls = [article["url"] for article in _data["articles"]]
        articles = self.content.get_content(urls)
        return articles

    def get_top(self, digest: Digest):
        if not digest: raise ValueError("Digest not specified")
        _data = self._get_newsapi(
            digest,
            self.cli.get_top_headlines,
            country="us"
        )
        urls = [article["url"] for article in _data["articles"]]
        articles = self.content.get_content(urls)
        return articles