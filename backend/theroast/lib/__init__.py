import newspaper
from newspaper import news_pool
import time

urls = [
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',  
]

class SingleSource(newspaper.Source):
    def __init__(self, articleURL):
        super(SingleSource, self).__init__("http://localhost")
        self.articles = [newspaper.Article(url=articleURL)]

sources = [SingleSource(articleURL=u) for u in urls]

s = time.time()

news_pool.set(sources, threads_per_source=2)
news_pool.join()

for source in sources:
    for article in source.articles:
        article.parse()

# for url in urls:
#     article = newspaper.Article(url)
#     article.download()
#     article.parse()

print(time.time() - s)