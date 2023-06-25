from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.chat_models import ChatOpenAI, ChatAnthropic
from theroast.config import OPENAI_API_KEY, ANTHROPIC_API_KEY

import json
from theroast.theroast.lib.prompts import collate, section

def section_request(ag, sections, personality):

    sects = []
    for k, v in sections.items():
        
        sm, sp = section.SectionPrompt().create_prompt(v, personality)
        is_valid = False
        sect = {}
        while not is_valid:
            section__raw: AIMessage = ag.predict_messages([
                SystemMessage(content = sm),
                HumanMessage(content = sp)
            ])
            try:
                sect = json.loads(section__raw.content)
                is_valid = True
            except json.JSONDecodeError:
                print(section__raw.content)
                continue
        sects.append(sect)

    return sects

def collate_request(ag, sections, personality):

    sm, cp = collate.CollatePrompt().create_prompt(sections, personality)

    is_valid = False
    coll = {}
    while not is_valid:
        collate__raw: AIMessage = ag.predict_messages([
            SystemMessage(content = sm),
            HumanMessage(content = cp)
        ])
        try:
            coll = json.loads(collate__raw.content)
            is_valid = True
        except json.JSONDecodeError:
            print(collate__raw.content)
            continue

    return coll