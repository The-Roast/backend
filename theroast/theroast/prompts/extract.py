from . import Prompt
from textwrap import dedent

EXTRACT_PROMPT = dedent('''\
    Given the comma-separated list of headlines separated by <>, determine and cluster the most important articles a person should read to get an accurate and full summary of the days events based on the articles provided. \
    Format your response as a JSON.
    To effectively complete this task, follow the "extract_and_cluster_articles" procedure where anything in {} is for you to decide:
    procedure extract_and_cluster_articles(list_of_headlines: List[String]):
        if {list_of_headlines is in an invalid format}:
            return {"message": "Invalid format"}
        json = {"sections": []}
        important_headlines: List[String] = {Extract only the most important headlines from the list_of_headlines}
        num_sections: Integer = {Determine the optimal number of sections based on the similarity of the important_headlines and their topic/theme/category choice}
        sections: List[List[String]] = []
        for i in 1...num_sections:
            section: List[String] = {Extract the fewest and most similar headlines from important_headlines}
            for-each headline in section:
                important_headlines.remove(headline)
            sections.append(section)
        json["sections"] = sections
        return json
    ''')

'''
Given the user response separated by <>, the previous hardcoded response separated by [[]] and the comma-separated list of posssible hardcoded responses to select from separated by (()), give an appropriate response to the user to help engage them in meaningful conversation and promote cognition, independence and wellbeing.
To effectively complete this task, follow the "generate_response" procedure where anything in {} is for you to decide:
procedure generate_response(user_response, previous_hardcoded_response, possible_hardcoded_responses):
    background_response: String = {Based on the user_response create meaningful and appreciative sentences acknowledging what they said}
    possible_hardcoded_responses.remove(previous_hardcoded_response)
    next_hardcoded_response: String = {Based on the user_response and the previous_hardcoded_response select the next hardcoded response to give to the user to help engage the user in meaningful conversation and promote cognition, independence and wellbeing}
    transition_sentences: String = {Create a transition that maintains the tone of the background_response and is a cohesive transition to the next_hardcoded_response}
    final_response = background_response + transition_sentences + next_hardcoded_response
    return final_response
'''