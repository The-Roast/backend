import datetime
from typing import List
from ..schemas import Articles, Newsletters

def create_articles(news, newsletters: List[Newsletters] = None):

    articles = []
    for i, article in enumerate(news["articles"]):
        published_at = datetime.datetime.strptime(article[""],"%Y-%m-%dT%H:%M:%S.%fZ")
        published_at = published_at.strftime("%Y-%m-%dT%H")
        articles.append(Articles(
            newsletters = newsletters,
            source_id = article["source"]["id"],
            source_name = article["source"]["name"],
            author = article["author"],
            title = article["title"],
            content = article["content"],
            url = article["url"],
            published_at = published_at
        ))
    return articles

def get_articles_by_url(urls):
    return Articles.query.filter_by(Articles.url.in_(urls)).all()

def get_articles_by_source_id(source_ids):
    return Articles.query.filter_by(Articles.source_id.in_(source_ids)).all()

def get_articles_by_source_name(source_names):
    return Articles.query.filter_by(Articles.source_name.in_(source_names)).all()

def get_articles_by_author(authors):
    return Articles.query.filter_by(Articles.author.in_(authors)).all()