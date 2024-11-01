# actions.py
import random
from typing import Any, Text, Dict, List
import yaml

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionKeywordResponse(Action):
    def name(self) -> Text:
        return "action_keyword_response"

    @staticmethod
    def load_keywords(file_path: Text) -> List[Dict[Text, Any]]:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data.get('keywords', [])

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        keyword = next(tracker.get_latest_entity_values("keyword"), None)
        if keyword:
            keywords = self.load_keywords('data/keywords/keywords.yml')
            for item in keywords:
                if item['keyword'] == keyword:
                    responses = item.get('responses', [])
                    if responses:
                        response = random.choice(responses)
                        dispatcher.utter_message(text=response)
                        return []
            return []
