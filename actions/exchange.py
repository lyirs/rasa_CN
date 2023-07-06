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


class ActionExchangeRate(Action):

    def name(self) -> Text:
        return "action_exchange_rate"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        number = next(tracker.get_latest_entity_values("number"), None)

        # 发起 GET 请求
        url = 'http://op.juhe.cn/onebox/exchange/currency'
        params = {
            'key': os.getenv("Exchange_KEY", ""),
            'from': 'USD',
            'to': 'CNY',
            'version': 2,
        }
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

        info = f"当前汇率：{data['result'][0]['exchange']}\n(结果：{result})"

        dispatcher.utter_message(text=info)

        return []
