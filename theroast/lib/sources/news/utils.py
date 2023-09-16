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

def convert_datetime_to_str(news_in: list):

    for i, a in enumerate(news_in):
        news_in[i]["published_at"] = news_in[i]["published_at"].strftime("%m/%d/%Y, %H:%M:%S")
    return news_in