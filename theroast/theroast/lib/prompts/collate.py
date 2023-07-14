from . import Prompt, SYSTEM_PROMPT
from textwrap import dedent

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
    Given the broken JSON, reformat it so that it follows the formatting and is a parseable JSON. Format your response as a JSON with the following structure:
    {
        "title": "Title of newsletter",
        "introduction": "Introduction of newsletter",
        "conclusion": "Conclusion of newsletter"
    }
    ''')

class CollatePrompt(Prompt):

    def create_prompt(self, sections, personality):

        assert sections and isinstance(sections, list)

        sy = SYSTEM_PROMPT.replace("{PERSONALITY}", personality if personality else "typical").replace("{INTERESTS}", "NBA")
        sp = f"{COLLATE_PROMPT}\n<" + "\t".join([f"{s['title']}\n{s['body']}" for s in sections]) + ">"

        return sy, sp

    def reformat_prompt(self, json):

        assert json

        return f"{REFORMAT_COLLATE_PROMPT}\n${json}$"
