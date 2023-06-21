from . import Prompt
from textwrap import dedent

EXTRACT_PROMPT = dedent('''\
    Given the tab-separated list of headlines separated by <>, determine the most important articles a person should read for a comprehensive and digestable newsletter of the days events. Format your response as a JSON with the following structure:
    {
        "headlines": ["list", "of", "important", "headlines", "the", "user", "should", "know", "about"]
    }
    To effectively complete this task, follow the "extract_articles" procedure where anything in {} is for you to decide:
    procedure extract_articles(list_of_headlines: List[String]):
        if {list_of_headlines is in an invalid format}:
            return {"message": "Invalid format"}
        json = {"headlines": []}
        important_headlines: List[String] = list_of_headlines
        while len(important_headlines) > 20:
            important_headlines: List[String] = {Extract the most important headlines from the important_headlines that are comprehensive for summarizing the days events to the user}
        json["headlines"] = sections
        return json
    ''')
REFORMAT_EXTRACT_PROMPT = dedent('''\
    Given the broken JSON separated by $$, reformat it so that it follows the formatting and is a parseable JSON. Format your response as a JSON with the following structure:
    {
        "headlines": ["list", "of", "important", "headlines", "the", "user", "should", "know", "about"]
    }
    ''')

class ExtractPrompt(Prompt):

    def create_prompt(self, headlines):

        assert headlines and isinstance(headlines, list)

        return f"{EXTRACT_PROMPT}\n<" + "\t".join(headlines) + ">"

    def reformat_prompt(self, json):

        assert json

        return f"{REFORMAT_EXTRACT_PROMPT}\n${json}$"