'''Config file defining all environment variables for use'''

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(".flaskenv"))

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

ENV = os.getenv("FLASK_ENV")
DEBUG = ENV == "development"
SECRET_KEY = os.getenv("SECRET_KEY")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

CELERY = {
    "broker_url": os.getenv("CELERY_BROKER_URL"),
    "result_backend": os.getenv("RESULT_BACKEND"),
}

DB_USERNAME = os.getenv("POSTGRESQL_USERNAME")
DB_PASSWORD = os.getenv("POSTGRESQL_PASSWORD")
DB_NAME = os.getenv("POSTGRESQL_DATABASE")

SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@localhost:5432/{DB_NAME}"

MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_PORT = os.getenv("MAIL_PORT")
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
MAIL_USE_SSL = os.getenv("MAIL_USE_SSL")
