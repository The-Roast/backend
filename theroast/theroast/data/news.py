from datetime import date
from newsapi import NewsApiClient, newsapi_exception
from ...config import NEWS_API_KEY

SOURCES = ['https://abcnews.go.com', 'http://www.aljazeera.com', 'http://arstechnica.com',
           'https://apnews.com/', 'https://www.axios.com', 'http://www.bleacherreport.com',
           'http://www.bloomberg.com', 'http://www.breitbart.com', 'http://www.businessinsider.com',
           'https://www.buzzfeed.com', 'http://www.cbsnews.com', 'http://us.cnn.com',
           'http://cnnespanol.cnn.com/', 'https://www.ccn.com', 'https://www.engadget.com',
           'http://www.ew.com', 'https://www.espn.com', 'http://www.espncricinfo.com/',
           'http://fortune.com', 'http://www.foxnews.com', 'http://www.foxsports.com',
           'https://news.google.com', 'https://news.ycombinator.com', 'http://www.ign.com',
           'https://mashable.com', 'http://www.medicalnewstoday.com', 'http://www.msnbc.com',
           'http://www.mtv.com/news', 'http://news.nationalgeographic.com', 'https://www.nationalreview.com/',
           'http://www.nbcnews.com', 'https://www.newscientist.com/section/news', 'https://www.newsweek.com',
           'http://nymag.com', 'https://www.nextbigfuture.com', 'http://www.nfl.com/news',
           'https://www.nhl.com/news', 'https://www.politico.com', 'http://www.polygon.com',
           'http://www.recode.net', 'https://www.reddit.com/r/all', 'http://www.reuters.com',
           'https://techcrunch.com', 'http://www.techradar.com', 'http://www.theamericanconservative.com/',
           'http://thehill.com', 'http://www.huffingtonpost.com', 'http://thenextweb.com',
           'http://www.theverge.com', 'http://www.wsj.com', 'https://www.washingtonpost.com',
           'https://www.washingtontimes.com/', 'http://time.com', 'http://www.usatoday.com/news',
           'https://news.vice.com', 'https://www.wired.com']

def extract_headlines(articles):

    '''Method for extracting descriptions in a format ready for LLM'''

    assert articles

    return list(articles.keys())

def process_articles(articles):

    '''Method for processing articles into a dictionary corresponding headlines to content'''
    print(articles)
    assert articles

    return {a["title"]: a["content"] for a in articles["articles"]}

def extract_articles(articles, section):

    '''Method for extracting articles based on corresponding id numbers'''

    assert articles

    content = {}
    for k, v in section.items():
        content[k] = [articles["articles"][i] for i in v]

    return content

class NewsScraper:

    '''Wrapper class for scraping news using NewsAPI'''

    def __init__(self):

        self.cli = NewsApiClient(NEWS_API_KEY)

    def get_everything(self, q, sources):

        '''Method for getting all news articles with a specific query'''

        assert self.cli
        assert q

        today = date.today()
        articles = {}
        c = 0

        while c < 3:
            try:
                articles = self.cli.get_everything(
                    q = q,
                    # sources = ",".join(sources) if len(sources) > 0 else None,
                    from_param = f"{today.year:04}-{today.month:02}-{(today.day-2):02}",
                    language = "en",
                    sort_by = "relevancy",
                )
                print("line 81 news.py", articles)
                break
            except newsapi_exception.NewsAPIException as e:
                print(e)
                c += 1

        return articles

    def get_category(self, q, c):

        '''Method for getting all news articles with a specific query and category'''

        assert self.cli
        assert q or c

        c = 0
        articles = {}

        while c < 3:
            try:
                articles = self.cli.get_top_headlines(
                    q = q,
                    language = "en",
                    country = "us",
                    category = c,
                )
                break
            except newsapi_exception.NewsAPIException as e:
                c += 1

        return articles

    @staticmethod
    def get_sources():
        
        return ['https://abcnews.go.com',
                'http://www.aljazeera.com',
                'http://arstechnica.com',
                'https://apnews.com/',
 'https://www.axios.com',
 'http://www.bleacherreport.com',
 'http://www.bloomberg.com',
 'http://www.breitbart.com',
 'http://www.businessinsider.com',
 'https://www.buzzfeed.com',
 'http://www.cbsnews.com',
 'http://us.cnn.com',
 'http://cnnespanol.cnn.com/',
 'https://www.ccn.com',
 'https://www.engadget.com',
 'http://www.ew.com',
 'https://www.espn.com',
 'http://www.espncricinfo.com/',
 'http://fortune.com',
 'http://www.foxnews.com',
 'http://www.foxsports.com',
 'https://news.google.com',
 'https://news.ycombinator.com',
 'http://www.ign.com',
 'https://mashable.com',
 'http://www.medicalnewstoday.com',
 'http://www.msnbc.com',
 'http://www.mtv.com/news',
 'http://news.nationalgeographic.com',
 'https://www.nationalreview.com/',
 'http://www.nbcnews.com',
 'https://www.newscientist.com/section/news',
 'https://www.newsweek.com',
 'http://nymag.com',
 'https://www.nextbigfuture.com',
 'http://www.nfl.com/news',
 'https://www.nhl.com/news',
 'https://www.politico.com',
 'http://www.polygon.com',
 'http://www.recode.net',
 'https://www.reddit.com/r/all',
 'http://www.reuters.com',
 'https://techcrunch.com',
 'http://www.techradar.com',
 'http://www.theamericanconservative.com/',
 'http://thehill.com',
 'http://www.huffingtonpost.com',
 'http://thenextweb.com',
 'http://www.theverge.com',
 'http://www.wsj.com',
 'https://www.washingtonpost.com',
 'https://www.washingtontimes.com/',
 'http://time.com',
 'http://www.usatoday.com/news',
 'https://news.vice.com',
 'https://www.wired.com']