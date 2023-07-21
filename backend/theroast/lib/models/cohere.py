import cohere
from theroast.lib.ai.models.base import MLBase
from theroast.config import api_config

class Cohere(MLBase):

    def __init__(self, config: dict = {}):
        self.model = cohere.Client(
            api_key=api_config.COHERE_API_KEY
            **config
        )
    
    def predict(self, data):
        return NotImplemented
    
    def rerank(self, query, data, model="rerank-english-v2.0"):
        return self.model.rerank(
            query=query,
            documents=data,
            model=model
        )

cohere = Cohere()