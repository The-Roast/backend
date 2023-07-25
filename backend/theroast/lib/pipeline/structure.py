from typing import List

def restructure(sections: List[dict], structure: dict, with_html: bool = False) -> dict:
    return {
        "title": structure["title"],
        "introduction": structure["introduction"],
        "body": sections,
        "conclusion": structure["conclusion"],
    }