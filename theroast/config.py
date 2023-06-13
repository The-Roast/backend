'''Config file defining all environment variables for use'''

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(".flaskenv"))

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
