import json
from datetime import datetime
from typing import Dict, Any
from theroast.lib.sources.news.client import NewsSource
from theroast.lib.sources.news.utils import convert_datetime_to_str

def main():
    news = NewsSource()

    news_out = {}

    # Query

    # config_in: Dict[str, Any] = {}
    # config_in["interests"] = ["tech"]
    # config_in["sources"] = []
    # news_out = convert_datetime_to_str(news.get_all(config_in))

    # Category

    config_in: Dict[str, Any] = {}
    config_in["interests"] = ["tech"]
    config_in["sources"] = []
    config_in["category"] = "business"

    json.dump(news_out, open(f"scrapes/{datetime.now().timestamp()}.json", "w+"))

if __name__ == "__main__":
    main()