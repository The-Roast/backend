
from textwrap import dedent
from . import Prompt

SYSTEM_PROMPT = '''You are an unbiased formal newletter writer writing a piece meant to engage the reader and summarize the days content.'''

SECTION_PROMPT = dedent('''\
    Given the list of articles separated by <>, I want you to create a section of a newsletter solely based on the information within the list of articles provided.

    This section should be detailed and comprehensive detailing the main points of each article in list of articles that a reader of a newsletter would find interesting to learn about. \
    The section should not require the reader to view the article to understand anything brought up in the section. \
    There should be no introduction, conclusion, hooks and signposting in the section. \
    The personality you have should be subtly evident in the tone and mood of the writing style in the section. \
    If you use information you must cite the article you extracted the information from using [${number}] notation where the number is the index number of the article in the list provided. \

    I also want you to create a section header for the section.

    I want your response to be formatted as strictly a JSON with the following structure:
    {
        "title": "Section header you generated",
        "body": "Final section you generated"
    }''')
REFORMAT_SECTION_PROMPT = dedent('''\
    Given the broken JSON separated by $$, reformat it so that it follows the formatting and is a parseable JSON. Format your response as a JSON with the following structure:
    {
        "title": "Section header you generated",
        "body": "Final section you generated"
    }''')

class SectionPrompt(Prompt):

    def system(self, personality):
        system = f"{SYSTEM_PROMPT} As a writer you are {personality}." if personality else SYSTEM_PROMPT
        return system

    def human(self, articles):
        human = f"{SECTION_PROMPT}\n<" + "\n".join([f'({a})' for a in articles]) + ">"
        return human

    def reformat(self, json):
        return f"{REFORMAT_SECTION_PROMPT}\n${json}$"