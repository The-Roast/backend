from . import Prompt, SYSTEM_PROMPT
from textwrap import dedent

COLLATE_PROMPT = dedent('''\
    Given the tab-separated list of sections separated by <>, create structured, cohesive and comprehensive newletter such that a reader would be engaged and interested while reading. Format your response as a JSON with the following structure:
    {
        "title": "Title of newsletter",
        "introduction": "Introduction of newsletter",
        "conclusion": "Conclusion of newsletter"
    }
    To effectively complete this task, follow the "create_newsletter" procedure where anything in {} is for you to decide:
    procedure create_newsletter(list_of_sections: List[String]):
        if {list_of_sections is in an invalid format}:
            return {"message": "Invalid format"}
        json = {}
        json["title"]: String = {Create an engaging and descriptive title based on the list_of_sections (it should not be more than a couple of words)}
        json["introduction"]: String = {Create an engaging and descriptive introduction based on the list_of_sections and your personality}
        json["conclusion"]: String = {Create an engaging and descriptive conclusion based on the list_of_sections and your personality}
        return json
    ''')

class CollatePrompt(Prompt):

    def create_prompt(self, sections, personality):

        assert sections and isinstance(sections, list)

        sy = f"{SYSTEM_PROMPT} As a writer you are {personality}." if personality else SYSTEM_PROMPT
        sp = f"{COLLATE_PROMPT}\n<" + "\t".join(sections) + ">"

        return sy, sp
