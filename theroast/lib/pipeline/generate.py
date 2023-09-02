from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.chat_models.base import BaseChatModel
from typing import Dict, List, Tuple, Any
import json
import re
from ..prompts import (
    collate as collate_prompt,
    section as section_prompt,
    chat as chat_prompt
)
from datetime import datetime

START_CHAR = "{"
END_CHAR = "}"

def _predict_chat(ag: BaseChatModel, system: str, articles: str, history: List[dict], message: dict):
    _schema_map = {"agent": AIMessage, "human": HumanMessage}
    convo = [SystemMessage(system), HumanMessage(articles), AIMessage("Done.")]
    for hi_msg in history:
        convo.append(_schema_map[hi_msg["type"]](hi_msg["content"]))
    convo.append(_schema_map[message["type"]](message["content"]))
    str_response: AIMessage = ag.predict_messages(convo)
    di_response = {"type": "agent", "content": str_response.content, "created_at": datetime.now()}
    return di_response


def _parse_raw_json(content: str) -> Tuple[Dict[str, str], int]:
    """
    Process and parse JSON string from Agent into a dictionary.

    :param content: String to be parsed 
    :return: Dictionary of the parsed content
    """
    _num_modifications = 0
    
    start_idx = 0 if content[0] == START_CHAR else content.find("{")
    end_idx = len(content) if content[-1] == END_CHAR else content.rfind("}")
    if end_idx == -1 or end_idx < start_idx:
        raise ValueError("End character not in valid position.")
    content = content[start_idx:end_idx]
    _num_modifications += (start_idx) + (len(content) - end_idx)

    if "\\n" in content:
        content.replace("\\n", "\n")
    esc_content = content.encode("unicode-escape")
    # esc_content, ns0 = re.subn(rb"(\\n\\n)", rb"\\list", esc_content)
    esc_content, ns0 = re.subn(rb"\\n\\s*", rb"", esc_content)
    # esc_content, ns1 = re.subn(rb"(\\n)", rb"", esc_content)
    _num_modifications += ns0

    content = esc_content.decode("unicode-escape")

    content = content[1:-1].lstrip().rstrip()
    paired_content = re.split("\s*\"\s*,\s*\"\s*", content)
    paired_content = [re.split("\s*\"\s*:\s*\"\s*", pair) for pair in paired_content]
    if any([len(pair) != 2 for pair in paired_content]):
        raise ValueError("Invalid JSON attribute-value pairings.")
    li_content = []
    for i, pair in enumerate(paired_content):
        pair[1] = pair[1][0] + pair[1][1:-1].replace("\"", "\'") + pair[1][-1]
        for j, _str in enumerate(pair):
            pair[j] = pair[j].strip()
            pair[j] = pair[j] if pair[j].startswith("\"") else "\"" + pair[j]
            pair[j] = pair[j] if pair[j].endswith("\"") else pair[j] + "\""
        pair[j]
        li_content.append(":".join(pair))
    content = START_CHAR + ",".join(li_content) + END_CHAR

    print(content)
    di_content = json.loads(content)

    return di_content, _num_modifications

def _predict_message(ag: BaseChatModel, system: str, human: str) -> dict:
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
        str_response: AIMessage = ag.predict_messages([
            SystemMessage(content = system),
            HumanMessage(content = human)
        ])
        try:
            result, _num_modifications = _parse_raw_json(str_response.content)
            print(_num_modifications)
            is_valid = True
        except (json.JSONDecodeError, ValueError) as e:
            raw_str_response = f"Error parsing message: {str_response.content}"
            print(raw_str_response.encode("unicode_escape"))
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
        system = section_prompt.SectionPrompt().system(personality)
        human = section_prompt.SectionPrompt().human(v)
        di_section = _predict_message(ag, system, human)
        sections.append(di_section)
    return sections

def collate(ag: BaseChatModel, sections: List[str], personality: str) -> dict:
    """
    Collate sections based on the sections dictionary and personality.

    :param ag: Agent used for prediction
    :param sections: Dictionary of sections
    :param personality: The personality for the prompt creation
    :return: A dictionary of collated sections
    """
    system = collate_prompt.CollatePrompt().system(personality)
    human = collate_prompt.CollatePrompt().human(sections)
    return _predict_message(ag, system, human)

def chat(ag: BaseChatModel, articles: List[Dict[str, Any]], history: List[Dict[str, Any]], message: Dict[str, Any], personality: str) -> dict:
    system = chat_prompt.ChatPrompt().system(personality)
    articles = chat_prompt.ChatPrompt().article(articles)
    return _predict_chat(ag, system, articles, history, message)
