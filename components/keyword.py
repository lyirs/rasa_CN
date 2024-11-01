# custom_components.py

from typing import Any, Dict, Optional, Text, List
import yaml
from rasa.shared.nlu.constants import (INTENT)
from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.shared.nlu.constants import TEXT
from rasa.shared.nlu.training_data.message import Message


@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.INTENT_CLASSIFIER,
        DefaultV1Recipe.ComponentType.ENTITY_EXTRACTOR], is_trainable=False
)
class KeywordComponent(GraphComponent):
    name = "KeywordComponent"

    def __init__(self, config: Dict[Text, Any], keywords: List[Dict[Text, Any]]) -> None:
        self.config = config
        self.keywords = keywords

    @staticmethod
    def load_keywords(file_path: Text) -> List[Dict[Text, Any]]:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data.get('keywords', [])

    @staticmethod
    def get_default_config() -> Dict[Text, Any]:
        return {"keywords_file": "keywords.yml"}

    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: Any,
        resource: Any,
        execution_context: ExecutionContext,
    ) -> "KeywordComponent":
        keywords_file = config.get("keywords_file", "keywords.yml")
        keywords = cls.load_keywords(keywords_file)
        return cls(config, keywords)

    def process(self, messages: List[Message]) -> List[Message]:
        for message in messages:
            text = message.get(TEXT)
            for item in self.keywords:
                if item['keyword'] in text:
                    intent = {"name": "keyword_intent", "confidence": 1.0}
                    message.set(
                        INTENT, intent, add_to_output=True)
                    message.set("intent_ranking", [intent], add_to_output=True)
                    message.set(
                        "entities", [{"entity": "keyword", "value": item['keyword']}], add_to_output=True)
                    break
        return messages
