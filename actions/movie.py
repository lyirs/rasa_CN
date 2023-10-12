# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Dict, List, Text, Optional

from py2neo import Graph, NodeMatcher

class ActionRecommendMovie(Action):

    def name(self) -> Text:
        return "action_recommend_movie"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        graph = Graph("http://localhost:7474/browser/",auth = ('neo4j','12345678'),name='neo4j')
        movie_type = tracker.get_slot("movieType")