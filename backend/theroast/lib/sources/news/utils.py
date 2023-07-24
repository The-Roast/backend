def extract_articles(articles, section):
    '''Method for extracting articles based on corresponding id numbers'''
    if not articles or "articles" not in articles: raise ValueError("Invalid articles data")
    content = {}
    for key, value in section.items():
        content[key] = [articles["articles"][i] for i in value]
    return content