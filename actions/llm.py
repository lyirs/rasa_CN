import os
from typing import Any, Dict, List, Text, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import json
import openai


class ActionOpenai(Action):
    def name(self) -> Text:
        return "action_openai_fallback"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict]:

        client = openai.OpenAI(
            base_url=os.getenv(
                "OPENAI_URL", ""),
            api_key=os.getenv(
                "OPENAI_API", "")
        )

        message = [{"role": 'user', "content": tracker.latest_message['text']}]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=message,
            temperature=1.0
        )

        res = response.choices[0].message.content
        dispatcher.utter_message(text=res)

        return []
