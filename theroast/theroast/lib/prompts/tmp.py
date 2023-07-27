# import newspaper
# import json

# url = 'https://bleacherreport.com/articles/10082942-mlb-power-rankings-where-all-30-teams-stand-2-weeks-from-trade-deadline'
  
# article = newspaper.Article(url=url, language='en')
# article.download()
# article.parse()

article ={
    "title": str(article.title),
    "text": str(article.text),
    "authors": article.authors,
    "published_date": str(article.publish_date),
    "top_image": str(article.top_image),
    "videos": article.movies,
    "keywords": article.keywords,
    "summary": str(article.summary)
}


# print(article["title"] \
#      + "\n\t\t" + article["published_date"] \
#      + "\n\n"\
#      + "\n" + article["text"]\
#      + "\n\n")

import requests
from bs4 import BeautifulSoup

url = "https://bleacherreport.com/articles/10082942-mlb-power-rankings-where-all-30-teams-stand-2-weeks-from-trade-deadline"

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

article = soup.find('div', {'class': 'organism contentStream slideshow'})

paragraphs = article.find_all('p')

for p in paragraphs:
    print(p.text)