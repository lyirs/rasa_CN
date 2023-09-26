# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import time
import json
import requests
from typing import Any, Dict, List, Text, Optional
import datetime

with open('dataset/station_map.json', 'r', encoding='utf-8') as json_file:
    station_map = json.load(json_file)


def text_to_date(text_date: str) -> Optional[datetime.date]:
    today = datetime.datetime.now()
    one_more_day = datetime.timedelta(days=1)
    if text_date == "今天":
        return today.date()
    if text_date == "明天":
        return (today + one_more_day).date()
    if text_date == "后天":
        return (today + one_more_day * 2).date()
    if text_date == "大后天":
        return (today + one_more_day * 3).date()


class ActionQueryTrain(Action):

    def name(self) -> Text:
        return "action_query_train"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # 提取地点实体
        departure = tracker.get_slot("departure")
        destination = tracker.get_slot("destination")
        date_text = tracker.get_slot("date-time")

        date_object = text_to_date(date_text)

        departure_code = station_map.get(departure)
        destination_code = station_map.get(destination)

        if not departure_code or not destination_code:
            dispatcher.utter_message(text="我不知道这些地方的代码。")
            return []

        # 发起 GET 请求
        url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ'
        params = {
            'leftTicketDTO.train_date': date_object,
            'leftTicketDTO.from_station': departure_code,
            'leftTicketDTO.to_station': destination_code,
            'purpose_codes': 'ADULT',
        }
        headers = {
            'Cookie': '_uab_collina=163108019860709243490927; JSESSIONID=3A879F34238B594124705B10D7C0B0E6; BIGipServerotn=3956736266.64545.0000; guidesStatus=off; highContrastMode=defaltMode; cursorStatus=off; BIGipServerpassport=870842634.50215.0000; RAIL_EXPIRATION=1631354049020; RAIL_DEVICEID=jY49UGp1PWZZ0cY6CWj2wmKFDH60qsPXbu7L4D2DjNDJSM4sbqZmmlUm62-6L3k9SNtBAUgBPn7Rh1-FAxka97-nHNpT3QIh5YIXtw3mGao0mjLNkIv2ayvwqxWyFhdbos5_ziUA3XVil7awDZ0EjzKBAWdl22Hu; route=495c805987d0f5c8c84b14f60212447d; _jc_save_fromStation=%u957F%u6C99%2CCSQ; _jc_save_fromDate=2021-09-08; _jc_save_toDate=2021-09-08; _jc_save_wfdc_flag=dc; _jc_save_toStation=%u5CB3%u9633%u4E1C%2CYIQ',
            # 'Host': 'kyfw.12306.cn',
            # 'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E9%95%BF%E6%B2%99,CSQ&ts=%E5%B2%B3%E9%98%B3%E4%B8%9C,YIQ&date=2021-09-08&flag=N,N,Y',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url=url, params=params, headers=headers)

        if response.status_code != 200:
            dispatcher.utter_message(text="我无法从服务器获取数据。")
            return []

        data = response.json()

        if 'data' not in data or 'result' not in data['data'] or not data['data']['result']:
            dispatcher.utter_message(text="我没能找到火车信息。")
            return []

        # 提取火车信息
        train_info_list = []  # 创建一个空列表，用于存储所有的火车信息
        for train_data in data['data']['result']:
            result = train_data.split('|')

            train_no = result[3]  # 火车编号
            departure_city = departure  # 出发城市
            destination_city = destination  # 到达城市
            departure_time = result[8]  # 出发时间
            arrival_time = result[9]  # 到达时间

            # 将火车信息添加到列表中
            train_info_list.append(
                f"{train_no} {departure_city}-{destination_city} {departure_time}-{arrival_time}")

        # 将所有的火车信息合并成一条消息，并发送给用户
        dispatcher.utter_message(
            text='\n'.join(train_info_list))

        return []
