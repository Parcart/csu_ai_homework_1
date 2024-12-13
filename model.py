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
            SystemMessage(content='Ты ии ассистент для ЧелГУ, У тебя есть два варианта ответа[assistent,researcher]. Если вопрос касается ЧелГУ  используй  researcher и в сообщении генерируй запрос для поиска в поисковике, который более релевантно будет находить информацию в google, не уточняй у пользователя. Используй researcher во всех впорам о челгу. Если assistent отвечай сам. в формате json {"response_type": "assistent|researcher","message": "Ответ"}'),
            HumanMessage(content=query)
        ]
        return cls._invoke(messages)
    


if __name__ == "__main__":
    load_dotenv()
    print(LLMYandex.processing_query("Структуру хочу узнать"))
