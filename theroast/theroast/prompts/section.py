
from . import Prompt, SYSTEM_PROMPT
from textwrap import dedent

SECTION_PROMPT = dedent('''\
    Given the pipe-separated list of articles separated by <>, create a concise, comprehensive and detailed section of a newletter such that a reader would be engaged and interested while reading. Format your response as a JSON with the following structure:
    {
        "title": "Section Title",
        "body": "Body of section of newsletter"
    }
    To effectively complete this task, follow the "create_section" procedure where anything in {} is for you to decide:
    procedure create_section(list_of_articles: List[String]):
        if {list_of_articles is in an invalid format}:
            return {"message": "Invalid format"}
        json = {}
        json["title"]: String = {Create an engaging and descriptive title based on the list_of_articles (it should not be more than a couple of words)}
        body: String = ""
        for-each String article_to_summarize in list_of_articles:
            summary: String = {Create a couple of concise and engaging sentences that summarizes the main points of article_to_summarize and should standalone in that a person doesn't read the article_to_summarize or have prior context to understand the summary created or important events that occured in the day. Do not tell us what you are going to do or lead us on.}
            summary_with_personality = {Make summary fit with your personality as outlined in the system prompt. Do not be very obvious about the personality you have as it should only be subtly implied. It should maintain all information in summary only changing the tonality and mood of the writing. Note that it should still be concise, only being a two to three sentences at the very max. Do not tell us what you are going to do or lead us on.}
            summary_with_citation = {Add some transition text within summary_with_personality such that a citation can be placed at a token [CITATION]. For example, "Accordng to [CITATION], ..." would be fine.}
            hook: String = {Create an engaging phrase (only a few words) to hook the reader that connects back to the summary_with_personality. Add punctuation to transition to summary_with_personality at the end.}
            body = body + <b>hook</b> + summary + "\n\n"
        json["body"] = body
        return json
    ''')
REFORMAT_SECTION_PROMPT = dedent('''\
    Given the broken JSON separated by $$, reformat it so that it follows the formatting and is a parseable JSON. Format your response as a JSON with the following structure:
    {
        "title": "Section Title",
        "body": "Body of section of newsletter"
    }
    ''')

class SectionPrompt(Prompt):

    def create_prompt(self, articles, personality):

        assert articles and isinstance(articles, list)

        sy = f"{SYSTEM_PROMPT} As a writer you are {personality}." if personality else SYSTEM_PROMPT
        sp = f"{SECTION_PROMPT}\n<" + "|".join(articles) + ">"

        return sy, sp

    def reformat_prompt(self, json):

        assert json

        return f"{REFORMAT_SECTION_PROMPT}\n${json}$"