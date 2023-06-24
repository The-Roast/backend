import cohere
from langchain.chat_models import ChatOpenAI, ChatAnthropic
from sentence_transformers import SentenceTransformer
from ...config import COHERE_API_KEY, ANTHROPIC_API_KEY, OPENAI_API_KEY

co = cohere.Client(COHERE_API_KEY)
st = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
ant = ChatAnthropic(anthropic_api_key = ANTHROPIC_API_KEY, model = "claude-1", temperature = 0.4)
gpt = ChatOpenAI(openai_api_key = OPENAI_API_KEY, model = "gpt-3.5-turbo-16k", temperature = 0.5)
