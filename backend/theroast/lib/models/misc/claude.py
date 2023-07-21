from typing import List
from langchain.chat_models import ChatAnthropic
from langchain.schema import BaseMessage, AIMessage, SystemMessage, HumanMessage
from theroast.lib.ai.models.base import MLBase
from theroast.config import api_config

class Claude(MLBase):

    def __init__(self, config: dict):
        self.model: ChatAnthropic = ChatAnthropic(
            anthropic_api_key=api_config.ANTHROPIC_API_KEY,
            **config
        )

    def predict(self, msgs: List[BaseMessage]):
        assert len(msgs) > 0
        return self.model.predict_messages(msgs)


claude: Claude = Claude({
    "temperature": 0.4,
    "max_tokens_to_sample": 2048,
    "model": "claude-2"
})