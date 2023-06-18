from langchain.chat_models import ChatOpenAI

from theroast.theroast.data.news import NewsScraper, extract_headlines, process_articles
from theroast.config import OPENAI_API_KEY
from theroast.theroast.v1.reqs import extract_request, cluster_request, section_request, collate_request
import json

PERSONALITY = "smart and sarcastic but not condescending or overbearing, and never immature"

ns = NewsScraper()
articles = ns.get_everything(q = "politics")
articles = process_articles(articles)
headlines = extract_headlines(articles)
ag = ChatOpenAI(openai_api_key = OPENAI_API_KEY, model = "gpt-3.5-turbo-16k", temperature = 0)
extr = extract_request(ag, headlines)
print(extr)
clus = cluster_request(ag, extr["headlines"], PERSONALITY)
print(clus)
sects = section_request(ag, clus, PERSONALITY)
print(sects)
coll = collate_request(ag, sects, PERSONALITY)
print(coll)

newsletter = f'{coll["title"]}\n\n{coll["introduction"]}' + "\n\n".join([f"{s['title']}\n{s['body']}" for s in sects]) + f'\n\n{coll["conclusion"]}'
print(newsletter)
