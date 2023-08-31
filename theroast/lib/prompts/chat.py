from . import Prompt
from textwrap import dedent

SYSTEM_PROMPT = '''You are an unbiased formal newletter writer writing a piece meant to engage the reader and summarize the days content.'''

COLLATE_PROMPT = dedent('''\
    Given the tab-separated list of sections separated by <>, create a title, introduction and conclusion for a newsletter based on the list of sections provided.
    
    The title must be concise (only a few words) and pertanent to the list of sections.
    The introduction must be engaging and fun and provide a transition into the sections to be discussed.
    The conclusion must effectively summarize the main points of the list of sections and leave off on a good remark.

    Your response must be formatted as strictly a parsable JSON with the following structure.
    {
        "title": "Title of newsletter",
        "introduction": "Introduction of newsletter",
        "conclusion": "Conclusion of newsletter"
    }''')
REFORMAT_COLLATE_PROMPT = dedent('''\
    Given the broken JSON, reformat it so that it is parseable.
    ''')

class ChatPrompt(Prompt):

    def system(self):
        return ""

    def human(self):
        return ""
    
    def article(self):
        return ""

    def reformat(self, json):
        return f"{REFORMAT_COLLATE_PROMPT}\n${json}$"
