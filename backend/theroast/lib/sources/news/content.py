from typing import Optional, List
from newspaper import Article, Source, news_pool

class URLSource(Source):
    def __init__(self, url):
        super(URLSource, self).__init__("http://localhost")
        self.articles = [Article(url=url)]

class NewsContent():

    def __init__(self):
        self.sources: Optional[List[URLSource]] = None

    def _build_sources(self, urls: List[str], threads=2):
        if not urls: raise ValueError("URLs not specified")
        self.sources = [URLSource(url) for url in urls]
        news_pool.set(self.sources, threads)
        news_pool.join()

    def _process(self):
        if not self.sources: raise ValueError("Sources not initialized")
        articles = []
        for source in self.sources:
            if not source.articles:
                articles.append(None)
            article: Article = source.articles[0].parse()
            articles.append({
                "title": article.title,
                "content": article.text,
                "authors": article.authors,
                "published_at": article.publish_date,
                "url": article.url
            })
        return articles

    def get_content(self, urls):
        self._build_sources(urls)
        articles = self._process()
        return articles