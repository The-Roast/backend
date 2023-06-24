import cohere
from sentence_transformers import SentenceTransformer
from ...config import COHERE_API_KEY

co = cohere.Client(COHERE_API_KEY)
st = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')