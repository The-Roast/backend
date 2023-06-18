from langchain.chat_models import ChatOpenAI, ChatAnthropic
from theroast.theroast.data.news import NewsScraper, extract_headlines, process_articles
from theroast.config import OPENAI_API_KEY, ANTHROPIC_API_KEY
from theroast.theroast.v1.reqs import extract_request, cluster_request, section_request, collate_request
import json

def create_newsletter(ag, interests, sources, personality):

    ns = NewsScraper()
    news = ns.get_everything(q = " OR ".join(interests), sources = sources)
    
    articles = process_articles(news)
    headlines = extract_headlines(articles)

    extr = extract_request(ag, headlines)
    clus = cluster_request(ag, extr["headlines"], personality)
    ats = {}
    for k, v in clus.items():
        ats[k] = [articles[a] for a in v]
    sects = section_request(ag, ats, personality, news)
    coll = collate_request(ag, sects, personality)

    return sects, coll

def run_anthropic(interests, sources, personality):

    ag = ChatAnthropic(
        anthropic_api_key = ANTHROPIC_API_KEY,
        model = "claude-1",
        temperature = 0.4
    )
    return create_newsletter(ag, interests, sources, personality)

def run_openai(interests, sources, personality):

    ag = ChatOpenAI(
        openai_api_key = OPENAI_API_KEY,
        model = "gpt-3.5-turbo-16k",
        temperature = 0.5
    )
    return create_newsletter(ag, interests, sources, personality)