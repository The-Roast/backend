import markdown
from theroast.theroast.lib.extensions import ant, gpt
from theroast.theroast.data.news import NewsScraper, process_articles
from theroast.theroast.lib.reqs import section_request, collate_request
from theroast.theroast.lib.batch import extract_and_cluster

def create_newsletter(ag, interests, sources, personality):
    ns = NewsScraper()
    news = ns.get_everything(q = " OR ".join(interests), sources = sources)
    articles = process_articles(news)
    article__url = {a["content"]: [a["url"], a["source"]["name"]] for a in news["articles"]}
    clusters = extract_and_cluster(list(articles.values()), ",".join(interests), target = 30)
    sects, cc = section_request(ag, clusters, personality)
    coll = collate_request(ag, sects, personality)

    for i, c in enumerate(cc):
        sect = sects[i]
        for j, article in enumerate(c):
            sect["body"] = markdown.markdown(sect["body"].replace(f"[{j}]", f'<a href={article__url[article][0]}>({article__url[article][1]})</a>'))

    return sects, coll, articles

def chat(articles):
    pass

def run_anthropic(interests, sources, personality):
    return create_newsletter(ant, interests, sources, personality)

def run_openai(interests, sources, personality):
    return create_newsletter(gpt, interests, sources, personality)

sects, coll, articles = run_openai(["Politics"], [], "funny and humorous")

for sect in sects:
    print(sect)

print(coll)