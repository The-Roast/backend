
from textwrap import dedent
from . import Prompt, SYSTEM_PROMPT

SECTION_PROMPT = dedent('''\
    Given a list of article links separated by <>, assemble an engaging and insightful section for a newsletter. \
    This section should distill the essential points from each article in the list, resulting in a comprehensive summary that makes the original articles redundant for understanding.

    Eliminate elements such as introduction, conclusion, hooks, and signposting, but allow your personality to subtly influence the tone and mood of the writing in alignment with the dynamic system prompt.

    Cite any extracted information from the articles using the notation [${number}], where the number corresponds to the article's index in the list. \
    Aim for a seamless integration of these citations within the text.

    Additionally, formulate an engaging title for this section. The response must adhere to the JSON format that can be parsed by the Python json library, represented as:
    {
    "title": "Generated section title",
    "body": "Crafted section content"
    }

    The tone, ordering of the information, and the enticing nature of the section title should reflect the subject matter of the articles. \
    Incorporate both summarizations and direct quotes from the articles, favoring direct quotes where applicable.

    Ensure the newsletter content equally focuses on individual article content and also draws connections and synthesizes information across the articles. \
    Specific aspects such as the author's opinions, study results, or interview highlights should be emphasized where relevant. \
    Any biased aspects should be presented as the articles' opinions. \
    In cases of conflicting viewpoints across articles, present both perspectives, clearly indicating them as opinions from the respective articles.

    There is no hard limit on the length of the section, but maintain a balance to ensure it remains engaging to the reader.\
    ''')
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

        return sy, sp

    def reformat_prompt(self, json):

        assert json

        return f"{REFORMAT_SECTION_PROMPT}\n${json}$"