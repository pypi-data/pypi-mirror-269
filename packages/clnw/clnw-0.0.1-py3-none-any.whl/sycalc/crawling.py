
import requests
from bs4 import BeautifulSoup

import requests
from bs4 import BeautifulSoup

def News(keyword):
    url = 'https://search.naver.com/search.naver?where=news&query=' + keyword
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # 최신 뉴스 10개 추출
        news_list = soup.select('.news_area')

        # 결과 출력
        count = 0
        for news in news_list:
            title = news.select_one('.news_tit').text.strip()
            link = news.select_one('.news_tit')['href']
            print(f'{title}: {link}')
            count += 1
            if count >= 10:
                break
    else:
        print('네이버 뉴스에 접근할 수 없습니다.')

def Weather(address):

  html = requests.get(f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={address}+날씨")
  soup = BeautifulSoup(html.text, 'html.parser')

  address = soup.find('div', {'class':'title_area _area_panel'}).find('h2', {'class':'title'}).text
  print('위치 : ' + address)

  weather_data = soup.find('div', {'class':'weather_info'})

  temperature = weather_data.find('div', {'class':'temperature_text'}).text.strip()[5:]
  print('온도 : ' + temperature)

  weatherStatus = weather_data.find('span', {'class':'weather before_slash'}).text
  print('날씨 상태 : ' + weatherStatus)

  air = soup.find('ul', {'class':'today_chart_list'})
  infos = air.find_all('li', {'class':'item_today'})

  for info in infos:
    print(info.text.strip())

  print('-'*50)
  print("시간대 별 날씨 정보")
  weatherTime = soup.find_all('li', {'class':'_li'})
  for i in weatherTime:
    print(i.text.strip())
