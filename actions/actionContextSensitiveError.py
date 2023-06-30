from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher

class ActionContextSensitiveError(Action):

    def name(self) -> Text:
        return "action_context_sensitive_error"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # 获取最近的意图
        last_intent = tracker.latest_message['intent'].get('name')

        # 根据最近的意图选择上下文相关的错误回复
        if last_intent == "intent1":
            response = "抱歉，我没有理解您关于intent1的问题。请尝试重新提问。"
        elif last_intent == "intent2":
            response = "对不起，我无法回答您关于intent2的问题。请重新描述您的疑问。"
        else:
            dispatcher.utter_message(template="utter_default")
            return []

        # 发送上下文相关的错误回复
        dispatcher.utter_message(text=response)

        return []
