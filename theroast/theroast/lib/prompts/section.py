
from textwrap import dedent
from . import Prompt, SYSTEM_PROMPT
import inspect

SECTION_PROMPT = dedent('''\
    Given the list of articles separated by <>, I want you to create a section of a newsletter solely based on the information within the list of articles provided.

    This section should be detailed and comprehensive detailing the main points of each article in list of articles that a reader of a newsletter would find interesting to learn about. \
    The section should not require the reader to view the article to understand anything brought up in the section. \
    There should be no introduction, conclusion, hooks and signposting in the section. \
    The personality you have should be subtly evident in the tone and mood of the writing style in the section. \
    If you use information you must cite the article you extracted the information from using [${number}] notation where the number is the zero-based index of the article in the list provided. \

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

    def create_prompt(self, articles, personality):

        assert articles and isinstance(articles, list)

        sy = f"{SYSTEM_PROMPT} As a writer you are {personality}." if personality else SYSTEM_PROMPT
        sp = f"{SECTION_PROMPT}\n<" + "\n".join([f'({a})' for a in articles]) + ">"


        print(inspect.cleandoc(str(sy)))
        for a in articles:
            print(len(a))

        return sy, sp

    def reformat_prompt(self, json):

        assert json

        return f"{REFORMAT_SECTION_PROMPT}\n${json}$"