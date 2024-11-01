import os
from typing import Any, Dict, List, Text, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import json
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import WebBaseLoader, DirectoryLoader
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores import FAISS

from actions import ConfigLoader
config = ConfigLoader.get_config()


class ActionOpenai(Action):
    def name(self) -> Text:
        return "action_openai_fallback"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict]:

        _config = next(
            item for item in config['apis'] if item['name'] == 'OpenAI')
        url = _config['url']
        api_key = _config['key']

        llm = ChatOpenAI(
            openai_api_base=url,
            openai_api_key=api_key,
        )

        # 初始化 openai 的 embeddings 对象
        embeddings = OpenAIEmbeddings(
            openai_api_base=url,
            openai_api_key=api_key,
        )

        # res = llm.invoke("hi")
        # print(res)

        output_parser = StrOutputParser()

        loader = DirectoryLoader(
            'document', glob='**/*.txt')
        documents = loader.load()
        # 初始化加载器
        text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
        # 切割加载的 document
        split_docs = text_splitter.split_documents(documents)

        db = Chroma.from_documents(split_docs, embeddings)
        retriever = db.as_retriever()

        qa = RetrievalQA.from_chain_type(
            llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)

        result = qa({"query": tracker.latest_message['text']})

        res = result['result']
        dispatcher.utter_message(text=res)

        return []
