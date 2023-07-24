from typing import List, Dict, Any, Optional
import markdown
from ..models import CLAUDE, GPT
from ..sources.news import NewsSource 
from langchain.chat_models.base import BaseChatModel
from .generate import section, collate
from ...db.base import Digest
from .batch import batch

NEWS = NewsSource()
MODELS = {
    "CLAUDE": CLAUDE,
    "GPT": GPT
}

def scrape_articles(digest: Digest) -> List[Dict[str, Any]]:
    if not digest: raise ValueError("Digest not specified")
    query = " OR ".join(digest.interests)
    articles = NEWS.get_all(q=query, sources=digest.sources)
    return articles

def parse_markdown(sections, clusters, article_urls):
    html_sects = []
    for i, cluster in enumerate(clusters):
        sect_cntnt = sections[i]
        for j, article in enumerate(cluster):
            sect_cntnt["body"] = markdown.markdown(sect_cntnt["body"].replace(
                f"[{j}]",
                f'<a href={article_urls[article][0]}>({article_urls[article][1]})</a>'
            ))
        html_sects.append(sect_cntnt)
    return html_sects

def run_model(agent: BaseChatModel, clusters, digest: Digest):
    """Runs the model to generate sections and collate requests"""
    sects, cc = section(agent, clusters, digest.personality)
    coll = collate(agent, sects, digest.personality)
    return sects, cc, coll

def generate_newsletter(
        articles: Optional[List[Dict[str, Any]]],
        digest: Digest,
        agent: str = "GPT"
    ):
    if not articles:
        articles = scrape_articles(digest)
    content = []
    article_url = {}
    for i, article in enumerate(articles):
        if not article:
            continue
        content.append(article["content"])
        article_url[article["content"]] = [article["url"], article["source"]["name"]]
    clusters = batch(content, ",".join(digest.sources), target=30)
    sections, clusters, structure = run_model(MODELS[agent], clusters, digest.personality)
    sections = parse_markdown(sections, clusters, article_url)
    return sections, structure
