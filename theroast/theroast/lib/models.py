import markdown
from theroast.theroast.lib.extensions import MODELS, NEWS
from theroast.theroast.data.news import NewsScraper, process_articles
from theroast.theroast.lib.reqs import section_request, collate_request
from theroast.theroast.lib.batch import extract_and_cluster
from theroast.theroast.lib.utils import construct_newsletter_html

def get_news(interests, sources):
    news = NEWS.get_everything(q = " OR ".join(interests), sources = sources)
    articles = process_articles(news)
    return news, articles

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

def generate_newsletter(news, articles, interests, personality, ag = "gpt"):

    art_ctnt = []
    art_url = {}
    for i, article in enumerate(articles):
        if not article:
            continue
        art_ctnt.append(article["text"])
        art_url[article["text"]] = [news["articles"][i]["url"], news["articles"][i]["source"]["name"]]
    clusters = extract_and_cluster(art_ctnt, ",".join(interests), target = 30)
    sections, cc, structure = run_openai(clusters, personality) if ag == "gpt" \
                                else run_anthropic(clusters, personality)
    sections = parse_markdown(sections, cc, art_url)

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

# news, articles = get_news(["politics"], [])
# sections, structure = generate_newsletter(news, articles, ["politics"], "serious", "gpt")
# structure["sections"] = sections

# construct_newsletter_html(structure)