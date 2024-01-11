import os
from typing import Any, Dict, List, Text, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import json


class ActionOpenai(Action):
    def name(self) -> Text:
        return "action_openai_fallback"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict]:

        params = {
            "data": tracker.latest_message['text']
        }

        # response = requests.post(url="http://127.0.0.1/api", params=params)
        response = requests.post(url=os.getenv(
            "OPENAI_API", ""), params=params)

        if response.status_code != 200:
            dispatcher.utter_message(text="服务器寄了捏。")
            return []

        res = response.json()
        res = res['res']
        dispatcher.utter_message(text=res)

        return []
