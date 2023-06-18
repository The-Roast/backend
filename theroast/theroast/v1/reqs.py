from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
import json
from theroast.theroast.prompts import extract, collate, cluster, section

def extract_request(ag, headlines):

    extract__raw: AIMessage = ag.predict_messages([
        HumanMessage(content = extract.ExtractPrompt().create_prompt(headlines))
    ])
    extr = {}
    try:
        extr = json.loads(extract__raw.content)
    except json.JSONDecodeError:
        extract__raw = ag.predict_messages([
            HumanMessage(content = extract.ExtractPrompt().create_prompt(headlines)),
            extract__raw,
            HumanMessage(content = extract.ExtractPrompt().reformat_prompt(extract__raw.content))
        ])
        extr = json.loads(extract__raw.content)
    return extr

def cluster_request(ag, headlines, personality):

    cluster__raw: AIMessage = ag.predict_messages([
        HumanMessage(content = cluster.ClusterPrompt().create_prompt(headlines, personality))
    ])
    clus = {}
    try:
        clus = json.loads(cluster__raw.content)
    except json.JSONDecodeError:
        cluster__raw = ag.predict_messages([
            HumanMessage(content = cluster.ClusterPrompt().create_prompt(headlines, personality)),
            cluster__raw,
            HumanMessage(content = cluster.ClusterPrompt().reformat_prompt(cluster__raw.content))
        ])
        clus = json.loads(cluster__raw.content)
    return clus

def section_request(ag, sections, personality):

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
            section__raw = ag.predict_messages([
                SystemMessage(content = sm),
                HumanMessage(content = sp), 
                section__raw,
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
        collate__raw = ag.predict_messages([
            SystemMessage(content = sm),
            HumanMessage(content = cp),
            collate__raw,
            HumanMessage(content = collate.CollatePrompt().reformat_prompt(collate__raw.content))
        ])
        coll = json.loads(collate__raw.content)
    return coll