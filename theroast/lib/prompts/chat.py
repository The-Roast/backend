from . import Prompt
from textwrap import dedent

SYSTEM_PROMPT = dedent('''\
    You are a chatbot who responds to questions posited by a user using information provided within the provided articles. \
    If a question is given that is not related to any of the articles you are to response with the following extremely concise response: "Sorry, I don't know the answer to that question!" followed by a search query for web browsers to help find the answer to said question. \
    If you do not and can not provide a definitive answer based on the articles provided you should respond with the following extremely concise response: "Sorry, I don't know the answer to that question!" followed by a search query for web browsers to help find the answer to said question. \
    If you understand these instructions, respond with "Done."''')

REFORMAT_PROMPT = dedent('''\
    Given the broken JSON, reformat it so that it is parseable.
    ''')

class ChatPrompt(Prompt):

    def system(self, personality):
        return SYSTEM_PROMPT

    def human(self):
        return NotImplementedError
    
    def article(self, articles):
        return "<" + ",".join([f'({articles["content"]})']) + ">"

    def reformat(self, json):
        return NotImplementedError
