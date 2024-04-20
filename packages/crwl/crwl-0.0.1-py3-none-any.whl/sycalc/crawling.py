
import requests
from bs4 import BeautifulSoup

def search_news(keyword):
    base_url = "https://search.naver.com/search.naver?where=news&query="
    url = base_url + keyword

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # 기사 제목, 링크 가져오기
        news_titles = soup.find_all('a', {'class': 'news_tit'})

        print("검색된 뉴스 url:")
        for title in news_titles:
            news_title = title.get_text()
            news_link = title['href']
            print(news_title, ":", news_link)

    else:
        print("웹페이지 접속 오류")
        return None
