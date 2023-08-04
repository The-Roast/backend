from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.chat_models.base import BaseChatModel
from typing import Dict, List
import json
from ..prompts import (
    collate as collate_prompt,
    section as section_prompt
)

def _predict_message(ag: BaseChatModel, system_content: str, human_content: str) -> dict:
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

def section(ag: BaseChatModel, clusters: Dict[int, List[str]], personality: str) -> List[dict]:
    """
    Create section based on the sections dictionary and personality.

    :param ag: Agent used for prediction
    :param clusters: Dictionary of clusters
    :param personality: The personality for the prompt creation
    :return: A tuple of sections and clusters
    """
    sections = []
    for k, v in clusters.items():
        sm, sp = section_prompt.SectionPrompt().create_prompt(v, personality)
        dict_sect = _predict_message(ag, sm, sp)
        sections.append(dict_sect)
    return sections

def collate(ag: BaseChatModel, sections: List[str], personality: str) -> dict:
    """
    Collate sections based on the sections dictionary and personality.

    :param ag: Agent used for prediction
    :param sections: Dictionary of sections
    :param personality: The personality for the prompt creation
    :return: A dictionary of collated sections
    """
    sm, cp = collate_prompt.CollatePrompt().create_prompt(sections, personality)
    return _predict_message(ag, sm, cp)