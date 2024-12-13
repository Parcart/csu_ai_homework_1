from bs4 import BeautifulSoup
import requests
from pydantic import BaseModel

class News(BaseModel):
    title: str
    text: str
    image: str
    link : str

    
def get_news() -> list[News]:
    array_news = list()
    response = requests.get("https://www.csu.ru/_api/web/lists/getByTitle('Новости')/items?$top=3&$orderby=Created desc")
    soup = BeautifulSoup(response.content, 'xml')
    names = soup.find_all('d:OData__x0410__x0431__x0437__x0430__x04')
    for name in names:
        soup_html_title = BeautifulSoup(name.text, 'html5lib')
        soup_html_text = BeautifulSoup(name.find_next("d:OData__x0421__x043e__x0434__x0435__x04").text, 'html5lib')
        soup_html_image = BeautifulSoup(name.find_next("d:OData__x0418__x043b__x043b__x044e__x04").find("d:Description").text, 'html5lib')
        soup_html_link = BeautifulSoup(name.find_next("d:ID").text, 'html5lib')
        array_news.append(News(title=soup_html_title.find("p").text,
                               text=soup_html_text.find("p").text,
                               image=soup_html_image.find("body").text,
                               link=f"https://www.csu.ru/Lists/List1/newsitem.aspx?ID={soup_html_link.find("body").text}"))
    return array_news
        
