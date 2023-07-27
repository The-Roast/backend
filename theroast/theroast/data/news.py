from datetime import datetime, timedelta
from newsapi import NewsApiClient, newsapi_exception
from ...config import NEWS_API_KEY
import json
from newspaper import Article
import os

SOURCES = json.load(open(os.getcwd() + "/theroast/theroast/data/sources.json", "r"))

def extract_headlines(articles):

    '''Method for extracting descriptions in a format ready for LLM'''

    assert articles

    return list(articles.keys())

def process_articles(articles):

    '''Method for processing articles into a dictionary corresponding headlines to content'''

    assert articles

    content = []
    for article in articles["articles"]:
        url = article["url"]
        try:
            _article: Article = Article(url=url, language='en')
            _article.download()
            _article.parse()
            content.append({
                "title": str(_article.title),
                "text": str(_article.text),
                "authors": _article.authors,
                "published_date": str(_article.publish_date),
                "top_image": str(_article.top_image),
                "videos": _article.movies,
                "keywords": _article.keywords,
                "summary": str(_article.summary)
            })
        except Exception as e:
            content.append(None)

    return content

def extract_articles(articles, section):

    '''Method for extracting articles based on corresponding id numbers'''

    assert articles

    content = {}
    for k, v in section.items():
        content[k] = [articles["articles"][i] for i in v]

    return content

class NewsScraper:

    '''Wrapper class for scraping news using NewsAPI'''

    def __init__(self):

        self.cli = NewsApiClient(NEWS_API_KEY)

    def get_everything(self, q, sources):

        '''Method for getting all news articles with a specific query'''

        assert self.cli
        assert q

        today = datetime.today() - timedelta(days = 1)
        articles = {}
        c = 0

        sources_modified = []
        for s in sources:
            s = s.lower()
            if s in SOURCES:
                sources_modified.append(SOURCES[s])
                continue
            elif s in SOURCES.values():
                sources_modified.append(s)
                continue
        sources = sources_modified

        while c < 3:
            try:
                articles = self.cli.get_everything(
                    q = q,
                    sources = ",".join(sources) if len(sources) > 0 else None,
                    exclude_domains = "google.com",
                    from_param = f"{today.year:04}-{today.month:02}-{(today.day-2):02}",
                    language = "en",
                    sort_by = "relevancy",
                )
                break
            except newsapi_exception.NewsAPIException as e:
                print(e)
                c += 1

        return articles

    def get_category(self, q, c):

        '''Method for getting all news articles with a specific query and category'''

        assert self.cli
        assert q or c

        c = 0
        articles = {}

        while c < 3:
            try:
                articles = self.cli.get_top_headlines(
                    q = q,
                    language = "en",
                    country = "us",
                    category = c,
                )
                break
            except newsapi_exception.NewsAPIException as e:
                c += 1

        return articles