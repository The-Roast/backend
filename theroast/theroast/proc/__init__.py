from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from theroast.theroast.data.news import NewsScraper, extract_headlines, process_articles
from theroast.theroast.prompts import extract, collate, cluster, section
from theroast.config import OPENAI_API_KEY
import json

PERSONALITY = "snarky and sarcastic"

ns = NewsScraper()
articles = ns.get_everything(q = "politics")
articles = process_articles(articles)
headlines = extract_headlines(articles)
ag = ChatOpenAI(openai_api_key = OPENAI_API_KEY, model = "gpt-3.5-turbo-16k", temperature = 1)
extract__raw = ag.predict_messages([HumanMessage(content = extract.ExtractPrompt().create_prompt(headlines))])
extr = dict(json.loads(extract__raw.content))
cluster__raw = ag.predict_messages([HumanMessage(content = cluster.ClusterPrompt().create_prompt(extr["headlines"], PERSONALITY))])
clus = dict(json.loads(cluster__raw.content))
sections = []
for k, v in clus.items():
    sm, sp = section.SectionPrompt().create_prompt(v, PERSONALITY)
    section__raw = ag.predict_messages([
        SystemMessage(content = sm),
        HumanMessage(content = sp)
    ])
    print(section__raw.content)
    sections.append(dict(json.loads(section__raw.content)))
list_of_sections = [f'{s["title"]}\n{s["body"]}' for s in sections]
sm, cp = collate.CollatePrompt().create_prompt(list_of_sections, PERSONALITY)
collate__raw = ag.predict_messages([
    SystemMessage(content = sm),
    HumanMessage(content = cp)
])
coll = dict(json.loads(collate__raw.content))

newsletter = f'{coll["title"]}\n\n{coll["introduction"]}' + "\n\n".join(list_of_sections) + f'\n\n{coll["conclusion"]}'
print(newsletter)
