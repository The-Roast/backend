from typing import List, Dict, Any, Optional, Tuple
import markdown
from theroast.lib.models import CLAUDE, GPT
from theroast.lib.sources.news import NEWS 
from langchain.chat_models.base import BaseChatModel
from .generate import section, collate
from theroast.db.base import Digest
from .batch import batch
from itertools import chain

MODELS = {
    "CLAUDE": CLAUDE,
    "GPT": GPT
}

def scrape_articles(digest: dict) -> List[Dict[str, Any]]:
    return NEWS.get_all(digest)

def parse_markdown(
        sections: List[dict],
        clusters: List[str], 
        urls: Dict[str, List[str]]
    ) -> List[dict]:
    html_sects = []
    for i, cluster in enumerate(clusters):
        sect_cntnt = sections[i]
        if not sect_cntnt:
            continue
        for j, article in enumerate(cluster):
            sect_cntnt["body"] = markdown.markdown(sect_cntnt["body"].replace(
                f"[{j}]",
                f'<a href={urls[article]["url"]}>({urls[article]["source"]})</a>'
            ))
        html_sects.append(sect_cntnt)
    return html_sects

def run_model(
        agent: BaseChatModel,
        clusters: List[List[str]],
        digest: dict
    ) -> Tuple[List[dict], dict]:
    sections = section(agent, clusters, digest["personality"])
    structure = collate(agent, sections, digest["personality"])
    return sections, structure

def generate_newsletter(
        digest: dict,
        articles: Optional[List[Dict[str, Any]]] = None,
        agent: str = "GPT"
    ) -> Tuple[List[dict], dict]:
    print(type(articles))
    if not digest: raise ValueError("Digest not specified")
    if not ("interests" in digest and digest["interests"]) and \
       not ("sources" in digest and digest["sources"]):
        raise ValueError("Digest not valid for use.")
    if not articles: articles = scrape_articles(digest)
    content_article = {}
    for i, article in enumerate(articles):
        if not article:
            continue
        content_article[article["content"]] = article
    clusters = batch(list(content_article.keys()), digest["interests"], target=30)
    sections, structure = run_model(MODELS[agent], clusters, digest)
    sections = parse_markdown(sections, list(clusters.values()), content_article)
    flat_clusters = chain.from_iterable(clusters.values())
    used_articles = [content_article[content] for content in flat_clusters]
    return sections, structure, used_articles
