'''Module defining abstract class Prompt'''

from abc import ABC, abstractmethod

class Prompt(ABC):

    '''Abstract class representing the prompt creation behavior'''



    @staticmethod
    @abstractmethod
    def system(*args, **kwargs):

        '''Abstract function representing prompt creation'''

    @staticmethod
    @abstractmethod
    def human(*args, **kwargs):

        '''Abstract function representing prompt creation'''

    @staticmethod
    @abstractmethod
    def reformat(*args, **kwargs):

        '''Abstract function representing JSON reformatting'''