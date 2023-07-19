import markdown
from theroast.theroast.lib.extensions import MODELS, NEWS
from theroast.theroast.data.news import NewsScraper, process_articles
from theroast.theroast.lib.reqs import section_request, collate_request
from theroast.theroast.lib.batch import extract_and_cluster

def get_news(interests, sources):
    news = NEWS.get_everything(q = " OR ".join(interests), sources = sources)
    return news

def parse_markdown(sections, clusters, article__url):

    parsed = []

    for i, c in enumerate(clusters):
        section = sections[i]
        for j, article in enumerate(c):
            section["body"] = markdown.markdown(section["body"].replace(
                f"[{j}]",
                f'<a href={article__url[article][0]}>({article__url[article][1]})</a>'
            ))
        parsed.append(section)
    
    return parsed

def generate_newsletter(news, interests, personality, ag = "gpt"):

    articles = [a["content"] for a in news["articles"]]
    article__url = {a["content"]: [a["url"], a["source"]["name"]] for a in news["articles"]}
    clusters = extract_and_cluster(articles, ",".join(interests), target = 30)
    sections, cc, structure = run_openai(clusters, personality) if ag == "gpt" \
                                else run_anthropic(clusters, personality)
    sections = parse_markdown(sections, cc, article__url)

    return sections, structure

def chat(articles):
    pass

def run_anthropic(clusters, personality):
    sects, cc = section_request(MODELS["claude"], clusters, personality)
    coll = collate_request(MODELS["claude "], sects, personality)
    return sects, cc, coll

def run_openai(clusters, personality):
    sects, cc = section_request(MODELS["gpt"], clusters, personality)
    coll = collate_request(MODELS["gpt"], sects, personality)
    return sects, cc, coll

news = get_news(["sneakers"], [])
sections, structure = generate_newsletter(news, ["sneakers"], "serious")

for sect in sections:
    print(sect)

print(structure)