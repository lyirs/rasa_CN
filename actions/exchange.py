# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import os
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from typing import Any, Dict, List, Text, Optional

from actions import ConfigLoader
config = ConfigLoader.get_config()

class ActionExchangeRate(Action):

    def name(self) -> Text:
        return "action_exchange_rate"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        currency_map = {
            "美元":"USD",
            "日元":"JPY",
            "欧元":"EUR",
            "英镑":"GBP",
            "韩元":"KER",
            "港币":"HKD",
            "卢布":"RUB",
        }

        # number = next(tracker.get_latest_entity_values("number"), None)
        number = tracker.get_slot("number")
        currency = tracker.get_slot("currency")
        
        _config = next(
            item for item in config['apis'] if item['name'] == 'Exchange')
        url = _config['url']
        api_key = _config['key']

        try:
            params = {
                'key': api_key,
                'from': currency_map[currency],
                'to': 'CNY',
            }
        except Exception as e:
            dispatcher.utter_message(text="暂时不清楚这个货币的汇率哦~")
            return
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        response = requests.get(url=url, params=params, headers=headers)

        if response.status_code != 200:
            dispatcher.utter_message(text="我无法从服务器获取数据。")
            return []

        data = response.json()
        result = float(data['result'][0]['result'])
        result = float(number) * result  # type: ignore
        result = round(result, 2)

        info = f"当前汇率\n{currency_map[currency]}->CNY\n{data['result'][0]['exchange']}\n(结果：{result})"

        dispatcher.utter_message(text=info)

        return []
