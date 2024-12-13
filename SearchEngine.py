import os

from googleapiclient.discovery import build

from dotenv import load_dotenv
from langchain_core.tools import Tool
from langchain_google_community import GoogleSearchAPIWrapper
from pydantic import BaseModel


class SearchResult(BaseModel):
    title: str
    link: str
    snippet: str


class SearchEngine:
    __search: GoogleSearchAPIWrapper = None
    __tool = None
    __search_params = {
        "filter": 0,
        "safe": "off",
    }

    @staticmethod
    def __search_engine(query):
        return SearchEngine.__search.results(query, 10, search_params=SearchEngine.__search_params)

    @classmethod
    def __get_tool(cls) -> Tool:
        if cls.__tool is None:
            cls.__search = GoogleSearchAPIWrapper()
            cls.__tool = Tool(
                name="google_search",
                description="Search Google for recent results.",
                func=cls.__search_engine,
            )
        return cls.__tool

    @classmethod
    def run(cls, query: str) -> list[SearchResult]:
        print("INFO: Search query: " + query)
        skipped_links = []
        result = []
        for item in cls.__get_tool().run(query):
            if len(result) >= 3 or item.get("Result", False):
                break
            if item["title"] == "Untitled":
                skipped_links.append(item["link"])
                continue
            result.append(SearchResult(**item))

        return result

        


if __name__ == "__main__":
    load_dotenv()
    answer = SearchEngine.run("Структура ЧелГУ: какие факультеты и институты входят в состав университета?")
    print(answer)
    pass
