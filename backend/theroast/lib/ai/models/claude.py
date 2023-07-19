from theroast.lib.ai.models.base import MLBase
from theroast.config import api_config

class Claude(MLBase):

    def __init__(self):
        self.api_key = api_config.ANTHROPIC_API_KEY
        