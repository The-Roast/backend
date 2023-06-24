from posixpath import supports_unicode_filenames
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.chat_models import ChatOpenAI, ChatAnthropic
from theroast.config import OPENAI_API_KEY, ANTHROPIC_API_KEY

import json
from theroast.theroast.lib.prompts import collate, section

gpt = ChatOpenAI(
        openai_api_key = OPENAI_API_KEY,
        model = "gpt-3.5-turbo-16k",
        temperature = 0.5
    )

def section_request(ag, sections, personality, news):

    sects = []
    for k, v in sections.items():
        
        sm, sp = section.SectionPrompt().create_prompt(v, personality)
        section__raw: AIMessage = ag.predict_messages([
            SystemMessage(content = sm),
            HumanMessage(content = sp)
        ])
        sect = {}
        try:
            sect = json.loads(section__raw.content)
        except json.JSONDecodeError:
            section__raw = gpt.predict_messages([
                SystemMessage(content = sm),
                HumanMessage(content = sp), 
                section__raw,
                SystemMessage(content = sm),
                HumanMessage(content = section.SectionPrompt().reformat_prompt(section__raw.content))
            ])
            sect = json.loads(section__raw.content)
        sects.append(sect)

    return sects

def collate_request(ag, sections, personality):

    sm, cp = collate.CollatePrompt().create_prompt(sections, personality)
    collate__raw: AIMessage = ag.predict_messages([
        SystemMessage(content = sm),
        HumanMessage(content = cp)
    ])
    coll = {}
    try:
        coll = json.loads(collate__raw.content)
    except json.JSONDecodeError:
        collate__raw = gpt.predict_messages([
            SystemMessage(content = sm),
            HumanMessage(content = cp),
            collate__raw,
            SystemMessage(content = sm),
            HumanMessage(content = collate.CollatePrompt().reformat_prompt(collate__raw.content))
        ])
        coll = json.loads(collate__raw.content)
    return coll