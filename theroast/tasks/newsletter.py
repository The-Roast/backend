from ..extensions import celery
from ..theroast.lib.models import run_openai

def create_newsletter(settings):

    sects, coll, _ = run_openai(
        list(settings["interests"]),
        list(settings["sources"]),
        settings["personality"]
    )
    response = coll
    for sect in sects:
        response[sect["title"]] = sect["body"]
    
    return response