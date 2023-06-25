'''Module defining abstract class Prompt'''

from abc import ABC, abstractmethod

SYSTEM_PROMPT = '''You are an unbiased newletter writer writing a piece meant to engage the reader and summarize the days content.'''

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