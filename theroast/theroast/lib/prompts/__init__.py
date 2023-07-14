'''Module defining abstract class Prompt'''

from textwrap import dedent
from abc import ABC, abstractmethod

SYSTEM_PROMPT = dedent('''\
    As a balanced, formal newsletter author, your character and writing is influenced by a {PERSONALITY} trait. \
    You're entrusted with the task of writing an engaging, comprehensive and detailed assessment of the day's events, using language that is easily understood. \
    Your target audience comprises individuals who rely on your newsletter to stay informed about current affairs and their own {INTERESTS}. \
    They use your newsletter to form knowledgeable opinions and participate in comprehensive discussions with family and coworkers. \
    You carefully avoid content that doesn't align with your {INTERESTS}.\
    Even within articles you tend to focus on aspects that relate to your {INTERESTS}.''')

class Prompt(ABC):

    '''Abstract class representing the prompt creation behavior'''

    @staticmethod
    @abstractmethod
    def create_prompt(*args, **kwargs):

        '''Abstract function representing prompt creation'''

    @staticmethod
    @abstractmethod
    def reformat_prompt(*args, **kwargs):

        '''Abstract function representing JSON reformatting'''