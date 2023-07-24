from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
import json
from ..prompts import CollatePrompt, SectionPrompt

def _predict_message(ag, system_content: str, human_content: str) -> dict:
    """
    Predict and parse a message given system and human content.

    :param ag: Agent used for prediction
    :param system_content: Content of system message
    :param human_content: Content of human message
    :return: The predicted message as a dictionary
    """
    is_valid = False
    result = {}
    while not is_valid:
        str_message: AIMessage = ag.predict_messages([
            SystemMessage(content = system_content),
            HumanMessage(content = human_content)
        ])

        try:
            result = json.loads(str_message.content)
            is_valid = True
        except json.JSONDecodeError:
            print(f"Error parsing message: {str_message.content}")
            continue
    return result

def section(ag, sections, personality):
    """
    Create section based on the sections dictionary and personality.

    :param ag: Agent used for prediction
    :param sections: Dictionary of sections
    :param personality: The personality for the prompt creation
    :return: A tuple of sections and clusters
    """
    clusters = []
    _sections = []
    for k, v in sections.items():
        sm, sp = SectionPrompt().create_prompt(v, personality)
        dict_sect = _predict_message(ag, sm, sp)
        _sections.append(dict_sect)
        clusters.append(v)
    return _sections, clusters

def collate(ag, sections, personality):
    """
    Collate sections based on the sections dictionary and personality.

    :param ag: Agent used for prediction
    :param sections: Dictionary of sections
    :param personality: The personality for the prompt creation
    :return: A dictionary of collated sections
    """
    sm, cp = CollatePrompt().create_prompt(sections, personality)
    return _predict_message(ag, sm, cp)