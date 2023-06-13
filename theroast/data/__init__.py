from theroast.data.news import NewsScraper, extract_headlines

ns = NewsScraper()
articles = ns.get_everything(q = "NBA")
print(extract_headlines(articles))