# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


import os
from typing import Any, Text, Dict, List
import yaml
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from typing import Any, Dict, List, Text, Optional


from actions import ConfigLoader
config = ConfigLoader.get_config()
class ActionNews(Action):

    def name(self) -> Text:
        return "action_get_news"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        _config = next(
            item for item in config['apis'] if item['name'] == 'News')
        url = _config['url']
        api_key = _config['key']

        params = {
            'key': api_key,
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
                f"{title}[{date}]")

        dispatcher.utter_message(
            text='\n'.join(info_list))

        return []


class ActionWeiboHot(Action):

    def name(self) -> Text:
        return "action_get_weibohot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        _config = next(
            item for item in config['apis'] if item['name'] == 'WeiboHot')
        url = _config['url']
        api_key = _config['key']

        params = {
            'key': api_key,
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
        for new_data in data['result']['list'][:10]:
            title = new_data['hotword']
            hotwordnum = new_data['hotwordnum']
            info_list.append(
                f"{title}(热度：{hotwordnum})")

        dispatcher.utter_message(
            text='\n'.join(info_list))

        return []


class ActionToutiaoHot(Action):

    def name(self) -> Text:
        return "action_get_toutiaohot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        _config = next(
            item for item in config['apis'] if item['name'] == 'ToutiaoHot')
        url = _config['url']
        api_key = _config['key']

        params = {
            'key': api_key,
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
        for new_data in data['result']['list'][:10]:
            title = new_data['word']
            hotwordnum = new_data['hotindex']
            info_list.append(
                f"{title}(热度：{hotwordnum})")

        dispatcher.utter_message(
            text='\n'.join(info_list))

        return []
