from . import Prompt
from textwrap import dedent

CLUSTER_PROMPT = dedent('''\
    Given the tab-separated list of headlines separated by <> and the personality for agent separated by [[]], cluster the articles into balanced, detailed and descriptive sections a reader would need for a structured, comprehensive and digestable newsletter of the days events. Format your response as a JSON with the following structure:
    {
        "Section Name": ["list", "of", "headlines", "that", "fit", "into", "this", "section"],
        "Section Name": ["list", "of", "headlines", "that", "fit", "into", "this", "section"],
        ...
        "Section Name": ["list", "of", "headlines", "that", "fit", "into", "this", "section"]
    }
    To effectively complete this task, follow the "cluster_articles" procedure where anything in {} is for you to decide:
    procedure cluster_articles(list_of_headlines: List[String], personality_for_agent: String):
        if {list_of_headlines or personality_for_agent is in an invalid format}:
            return {"message": "Invalid format"}
        json = {}
        number_of_clusters: Integer = {Determine the optimal number of clusters to make based on list_of_headlines and your central goal}
        while number_of_clusters > 0:
            cluster_of_headlines: List[String] = {Create a cluster of headlines based on list_of_headlines and your central goal}
            for-each String headline in cluster:
                list_of_headlines.remove(headline)
            section_name: String = {Create section name based on cluster_of_headlines so that it is engaging to the user and conforms to the desired personality_for_agent}
            json[section_name] = cluster_of_headlines
            number_of_clusters--
        return json
    ''')

class ClusterPrompt(Prompt):

    def create_prompt(self, headlines, personality):

        assert headlines and isinstance(headlines, list)

        prompt = f"{CLUSTER_PROMPT}\n<" + "\t".join(headlines) + ">"

        return prompt if len(personality) == 0 else prompt + f"\n[[{personality}]]"
