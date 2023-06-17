'''Config file defining all environment variables for use'''

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(".flaskenv"))

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

ENV = os.getenv("FLASK_ENV")
DEBUG = ENV == "development"
SECRET_KEY = os.getenv("SECRET_KEY")

DB_USERNAME = os.getenv("POSTGRESQL_USERNAME")
DB_PASSWORD = os.getenv("POSTGRESQL_PASSWORD")
DB_NAME = os.getenv("POSTGRESQL_DATABASE")

SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@localhost:5432/{DB_NAME}"