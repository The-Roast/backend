from theroast.theroast.lib.extensions import ant, gpt
from theroast.theroast.data.news import NewsScraper, process_articles
from theroast.theroast.lib.reqs import section_request, collate_request
from theroast.theroast.lib.batch import extract_and_cluster

def create_newsletter(ag, interests, sources, personality):

    ns = NewsScraper()
    news = ns.get_everything(q = " OR ".join(interests), sources = sources)   
    articles = process_articles(news)
    clusters = extract_and_cluster(list(articles.values()), ",".join(interests), target = 30)
    sects = section_request(ag, clusters, personality)
    coll = collate_request(ag, sects, personality)

    return sects, coll

def run_anthropic(interests, sources, personality):
    return create_newsletter(ant, interests, sources, personality)

def run_openai(interests, sources, personality):
    return create_newsletter(gpt, interests, sources, personality)

sects, coll = run_openai(["NBA"], [], "serious and professional")

print(coll["title"])
print(coll["introduction"])
for j in sects:
    print(j["title"])
    print(j["body"])
print(coll["conclusion"])