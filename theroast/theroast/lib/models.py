from theroast.theroast.lib.extensions import ant, gpt
from theroast.theroast.data.news import NewsScraper, process_articles
from theroast.theroast.lib.reqs import section_request, collate_request
from theroast.theroast.lib.batch import extract_and_cluster

def create_newsletter(ag, interests, sources, personality):

    ns = NewsScraper()
    news = ns.get_everything(q = " OR ".join(interests), sources = sources)
    
    articles = process_articles(news)
    clusters = extract_and_cluster(articles, ",".join(interests), target = 30)
    sects = section_request(ag, clusters, personality, news)
    coll = collate_request(ag, sects, personality)

    return sects, coll

def run_anthropic(interests, sources, personality):
    return create_newsletter(ant, interests, sources, personality)

def run_openai(interests, sources, personality):
    return create_newsletter(gpt, interests, sources, personality)