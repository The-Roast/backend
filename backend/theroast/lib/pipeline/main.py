from typing import List, Dict, Any, Optional, Tuple
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

def parse_markdown(sections: List[dict], clusters: List[str], urls: Dict[str, List[str]]) -> List[dict]:
    html_sects = []
    for i, cluster in enumerate(clusters):
        sect_cntnt = sections[i]
        if not sect_cntnt:
            continue
        for j, article in enumerate(cluster):
            sect_cntnt["body"] = markdown.markdown(sect_cntnt["body"].replace(
                f"[{j}]",
                f'<a href={urls[article][0]}>({urls[article][1]})</a>'
            ))
        html_sects.append(sect_cntnt)
    return html_sects

def run_model(agent: BaseChatModel, clusters: List[List[str]], digest: Digest) -> Tuple[List[dict], dict]:
    sections = section(agent, clusters, digest.personality)
    structure = collate(agent, sections, digest.personality)
    return sections, structure

def generate_newsletter(
        articles: Optional[List[Dict[str, Any]]],
        digest: Digest,
        agent: str = "GPT"
    ) -> Tuple[List[dict], dict]:
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
    sections, structure = run_model(MODELS[agent], clusters, digest.personality)
    sections = parse_markdown(sections, list(clusters.values()), article_url)
    return sections, structure
