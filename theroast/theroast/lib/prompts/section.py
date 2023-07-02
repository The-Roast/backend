
from textwrap import dedent
from . import Prompt, SYSTEM_PROMPT

SECTION_PROMPT = dedent('''\
    Given a list of news articles marked by "<>", create a comprehensive and engaging newsletter section by summarizing their key points, eliminating the need for the reader to refer back to the original pieces. \
    Any newline should Use the "\n" token to represent a newline in the text. \
    Cite each paraphrased or borrowed piece of information using the notation [${index}], where index refers to the 0-indexed position of the article in the list. \
    These citations should blend seamlessly into the text. Formulate a gripping title for this section that mirrors its main theme. \
    Balance summaries and exact quotes from the articles, giving precedence to quotes to enhance the reader experience. \
    Highlight noteworthy findings, author opinions, or key interview insights, remembering to attribute these views to the articles themselves, not the AI. \
    In case of contradictory views within the articles, include both, correctly attributing each to its source article. \
    While there is no stringent word limit, strive for balance to keep the reader engaged. \
    The resulting output must strictly adhere to the JSON format as follows:
    {
    "title": "Generated section title",
    "body": "Crafted section content"
    }''')
REFORMAT_SECTION_PROMPT = dedent('''\
    Given the broken JSON separated by $$, reformat it so that it follows the formatting and is a parseable JSON. Format your response as a JSON with the following structure:
    {
        "title": "Section header you generated",
        "body": "Final section you generated"
    }''')

class SectionPrompt(Prompt):

    def create_prompt(self, articles, personality, interests = None):

        assert articles and isinstance(articles, list)

        sy = SYSTEM_PROMPT.replace("{PERSONALITY}", personality if personality else "typical").replace("{INTERESTS}", "NBA")
        sp = f"{SECTION_PROMPT}\n<" + "\n".join([f'({a})' for a in articles]) + ">"

        return sy, sp

    def reformat_prompt(self, json):

        assert json

        return f"{REFORMAT_SECTION_PROMPT}\n${json}$"