def merge_meta_and_text(meta, text):
    
    merged_data = []
    for i, _m in enumerate(meta):
        if not text[i]:
            continue
        data = {**_m, **text[i]}
        merged_data.append(data)
    
    return merged_data
    