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


class ActionNutrient(Action):

    def name(self) -> Text:
        return "action_get_nutrient"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        food = tracker.get_slot("food")
        # 发起 GET 请求
        url = 'https://apis.tianapi.com/nutrient/index'
        params = {
            'key': os.getenv("TIANAPI_KEY", ""),
            'word': food,
            'mode': 0
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        response = requests.get(url=url, params=params, headers=headers)

        if response.status_code != 200:
            dispatcher.utter_message(text="我无法从服务器获取数据。")
            return []

        data = response.json()

        info_list = []  #
        for new_data in data['result']['list'][:5]:
            name = new_data['name']
            rl = new_data['rl']
            gai = new_data['gai']
            tei = new_data['tei']
            xin = new_data['xin']
            xi = new_data['xi']
            dbz = new_data['dbz']
            zf = new_data['zf']
            shhf = new_data['shhf']
            wssa = new_data['wssa']
            wsfc = new_data['wsfc']
            wsse = new_data['wsse']
            ssxw = new_data['ssxw']
            dgc = new_data['dgc']
            info_list.append(
                f"{name}[100mg]\n热量(大卡):{rl} 钙:{gai} 铁:{tei} 锌:{xin} 硒:{xi} 蛋白质:{dbz} 脂肪:{zf} 碳水化合物:{shhf} 维生素A:{wssa} 维生素C:{wsfc} 维生素E:{wsse} 膳食纤维:{ssxw} 胆固醇:{dgc}")

        dispatcher.utter_message(
            text='\n'.join(info_list))

        return []
