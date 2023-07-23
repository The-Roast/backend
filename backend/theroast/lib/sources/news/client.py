from typing import Callable, Optional
from datetime import date
from newsapi import NewsApiClient, newsapi_exception
import newspaper
from theroast.db.base import Digest
from theroast.config import api_config

class NewsSources():
    def __init__(self):
        """
        Source object with default methods for Getting Data.
        """
        if not api_config.NEWS_API_KEY: raise ValueError("NEWS_API_KEY not set")
        self.cli: NewsApiClient = NewsApiClient(api_config.NEWS_API_KEY)

    def _get_newsapi(self, digest: Digest, method: Callable, **kwargs):
        if not self.cli: raise ValueError("NewsApiClient not initialized")
        if not digest.interests: raise ValueError("Interests not specified")
        interests = " OR ".join(digest.interests)
        sources = ",".join(digest.sources)
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
        return self._get_newsapi(
            digest,
            self.cli.get_everything,
            from_param=f"{today.year:04}-{today.month:02}-{(today.day-2):02}",
            exclude_domains=EXCLUDE_DOMAINS
        )

    def get_top(self, digest: Digest):
        if not digest: raise ValueError("Digest not specified")
        return self._get_newsapi(
            digest,
            self.cli.get_top_headlines,
            country="us"
        )