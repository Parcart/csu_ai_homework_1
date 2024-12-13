from enum import Enum
import os
from typing import Sequence

from dotenv import load_dotenv
from langchain_community.llms.yandex import YandexGPT
from langchain_core.messages import BaseMessage as BaseMessageLangchain, SystemMessage, HumanMessage
from pydantic import BaseModel
from yandex_cloud_ml_sdk import YCloudML

from langchain.chains import LLMChain

from langchain_core.prompts import PromptTemplate

prompt = """
Ты ии ассистент для ЧелГУ.
 Если вопрос касается ЧелГУ  используй  researcher и в ответе сформулируй только поисковой запрос, который более релевантно будет находить информацию в google. Используй researcher во всех вопросам о челгу и не уточняй у пользователя дополнительную информацию. 
 Если можешь ответить сам, то используй assistent, но не прикладывай ссылок. Если нужно найти информацию, что касается информации о ЧелГУ то используй researcher и отвечай поисковым запросом, иначе отвечай пользователю, но не уточняя у него информацию и не спрашивая дополнительную информацию.
Формат ответа json {"response_type": "assistent|researcher","message": "Твой ответ"}
"""

# sdk = YCloudML(folder_id="", auth="<токен>")

# model = sdk.models.completions('yandexgpt')
# model = model.configure(temperature=0.5)
# result = model.run("Что такое небо?")


# for alternative in result:
#     print(alternative)

class ResponseType(Enum):
    assistent = "assistent"
    researcher = "researcher"

class LLMAnswer(BaseModel):
    response_type: ResponseType
    message: str

class LLMYandex:
    __client: YandexGPT = None

    @classmethod
    def __get_client(cls) -> YandexGPT:
        if LLMYandex.__client is None:
            LLMYandex.__client = YandexGPT()
        return LLMYandex.__client

    @classmethod
    def _invoke(cls, messages: Sequence[BaseMessageLangchain], **kwargs):
        result = cls.__get_client().invoke(messages)
        return result
    
    @classmethod
    def processing_query(cls, query: str) -> str:
        messages = [
            SystemMessage(content=prompt),
            HumanMessage(content=query)
        ]
        return cls._invoke(messages)
    


if __name__ == "__main__":
    load_dotenv()
    print(LLMYandex.processing_query("А пицка вкусная?"))
