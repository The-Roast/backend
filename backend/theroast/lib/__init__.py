import newspaper
from newspaper import news_pool

urls = [
'http://www.baltimorenews.net/index.php/sid/234363921',
'http://www.baltimorenews.net/index.php/sid/234323971',
'http://www.atlantanews.net/index.php/sid/234323891',
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
]

class SingleSource(newspaper.Source):
    def __init__(self, articleURL):
        super(SingleSource, self).__init__("http://localhost")
        self.articles = [newspaper.Article(url=articleURL)]

sources = [SingleSource(articleURL=u) for u in urls]

news_pool.set(sources)
news_pool.join()

for source in sources:
    print(source.articles)
    for article in source.articles:
        article.parse()
        print(article.title)