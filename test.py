import newspaper

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

newspaper.news_pool.set(sources)
newspaper.news_pool.join()

multi=[]
i=0
for s in sources:
    i+=1
    print(s.articles)
    try:
        (s.articles[0]).parse()
        txt = (s.articles[0])
        multi.append(txt)
    except:
        pass

print(txt)