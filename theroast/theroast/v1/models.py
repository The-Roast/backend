from langchain.chat_models import ChatOpenAI, ChatAnthropic
from theroast.theroast.data.news import NewsScraper, extract_headlines, process_articles
from theroast.config import OPENAI_API_KEY
from theroast.theroast.v1.reqs import extract_request, cluster_request, section_request, collate_request
import json

def create_newsletter(ag, interests, personality, model = "gpt-3.5-turbo-16k", temperature = 0.8):

    ns = NewsScraper()
    articles = ns.get_everything(q = "politics")
    articles = process_articles(articles)
    headlines = extract_headlines(articles)
    ag = ChatOpenAI(openai_api_key = OPENAI_API_KEY, model = model, temperature = temperature)
    extr = extract_request(ag, headlines)
    clus = cluster_request(ag, extr["headlines"], personality)
    sects = section_request(ag, clus, personality)
    coll = collate_request(ag, sects, personality)
