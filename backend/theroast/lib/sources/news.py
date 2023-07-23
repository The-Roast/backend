import os
import json
from datetime import date
from newsapi import NewsApiClient, NewsAPIException
from ...config import NEWS_API_KEY

class NewsScraper:
    '''Wrapper class for scraping news using NewsAPI'''
    
    def __init__(self):
        if not NEWS_API_KEY:
            raise ValueError("NEWS_API_KEY not set")
        
        self.cli = NewsApiClient(NEWS_API_KEY)

    def _get_data(self, query, sources, method, **kwargs):
        if not self.cli:
            raise ValueError("NewsApiClient not initialized")
        
        if not query:
            raise ValueError("Query not specified")

        sources = [SOURCES[s.lower()] for s in sources]
        for _ in range(MAX_TRIES):
            try:
                return method(
                    q=query,
                    sources=",".join(sources) if sources else None,
                    exclude_domains="google.com",
                    language="en",
                    sort_by="relevancy",
                    **kwargs,
                )
            except NewsAPIException as e:
                print(e)
        return {}

    def get_everything(self, query, sources):
        '''Method for getting all news articles with a specific query'''
        today = date.today()
        return self._get_data(
            query,
            sources,
            self.cli.get_everything,
            from_param=f"{today.year:04}-{today.month:02}-{(today.day-2):02}"
        )

    def get_category(self, query, category):
        '''Method for getting all news articles with a specific query and category'''
        if not category:
            raise ValueError("Category not specified")
            
        return self._get_data(query, category, self.cli.get_top_headlines, category=category, country="us")

def extract_headlines(articles):
    '''Method for extracting descriptions in a format ready for LLM'''
    if not articles:
        raise ValueError("No articles provided")
    return list(articles.keys())

def process_articles(articles):
    '''Method for processing articles into a dictionary corresponding headlines to content'''
    if not articles or "articles" not in articles:
        raise ValueError("Invalid articles data")
    return {a["title"]: a["content"] for a in articles["articles"]}

def extract_articles(articles, section):
    '''Method for extracting articles based on corresponding id numbers'''
    if not articles or "articles" not in articles:
        raise ValueError("Invalid articles data")

    content = {}
    for key, value in section.items():
        content[key] = [articles["articles"][i] for i in value]
    return content