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


class ActionNews(Action):

    def name(self) -> Text:
        return "action_get_news"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # 发起 GET 请求
        url = 'http://v.juhe.cn/toutiao/index'
        params = {
            'key': os.getenv("NEWS_KEY", ""),
            'type': 'top',
            'page': 1,
            'page_size': 10,
            'is_filter': 1
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
        for new_data in data['result']['data']:
            title = new_data['title']
            author = new_data['author_name']
            date = new_data['date']
            info_list.append(
                f"{title}(来源：{author})[{date}]")

        # 将所有的火车信息合并成一条消息，并发送给用户
        dispatcher.utter_message(
            text='\n'.join(info_list))

        return []
