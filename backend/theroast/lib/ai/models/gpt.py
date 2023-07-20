from typing import List
from langchain.chat_models import ChatOpenAI
from langchain.schema import BaseMessage, AIMessage, SystemMessage, HumanMessage
from theroast.lib.ai.models.base import MLBase
from theroast.config import api_config

class GPT(MLBase):

    def __init__(self, config: dict):
        self.model: ChatOpenAI = ChatOpenAI(
            openai_api_key=api_config.OPENAI_API_KEY,
            **config
        )

    def predict(self, msgs: List[BaseMessage]):
        assert len(msgs) > 0
        return self.model.predict_messages(msgs)


gpt: GPT = GPT({
    "temperature": 0.5,
    "max_tokens": 2048,
    "model": "claude-2"
})