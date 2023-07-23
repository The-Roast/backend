from typing import Callable, Optional
from datetime import date
from newsapi import NewsApiClient, newsapi_exception
import newspaper
from theroast.db.base import Digest
from theroast.config import api_config

MAX_TRIES = 3
EXCLUDE_DOMAINS = "google.com"
LANGUAGE = "en"

class NewsContent():
    pass



