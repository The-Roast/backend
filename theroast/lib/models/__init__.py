import cohere
from langchain.chat_models import ChatOpenAI
# ChatAnthropic
from sentence_transformers import SentenceTransformer
from theroast.config import api_config

COHERE = cohere.Client(api_config.COHERE_API_KEY)
ST_ENCODER = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
# CLAUDE = ChatAnthropic(anthropic_api_key=api_config.ANTHROPIC_API_KEY, model="claude-1", temperature=0.4)
GPT = ChatOpenAI(openai_api_key=api_config.OPENAI_API_KEY, model="gpt-3.5-turbo-16k", temperature=0.5)
CLAUDE = ChatOpenAI(openai_api_key=api_config.OPENAI_API_KEY, model="gpt-3.5-turbo-16k", temperature=0.5)