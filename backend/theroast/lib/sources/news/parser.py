def process_articles(articles):
    '''Method for processing articles into a dictionary corresponding headlines to content'''
    if not articles or "articles" not in articles:
        raise ValueError("Invalid articles data")
    return {a["title"]: a["content"] for a in articles["articles"]}

def extract_articles(articles, section):
    '''Method for extracting articles based on corresponding id numbers'''
    if not articles or "articles" not in articles:
        raise ValueError("Invalid articles data")

    content = {}
    for key, value in section.items():
        content[key] = [articles["articles"][i] for i in value]
    return content