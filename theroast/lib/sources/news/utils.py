from datetime import datetime

def merge_meta_and_text(meta, text):
    
    merged_data = []
    for i, _m in enumerate(meta):
        if not text[i]:
            continue
        text[i]["published_at"] = datetime.strptime(_m["publishedAt"][0:-1], "%Y-%m-%dT%H:%M:%S")
        data = {
            "source": _m["source"]["name"],
            **text[i]}
        merged_data.append(data)
    
    return merged_data
    