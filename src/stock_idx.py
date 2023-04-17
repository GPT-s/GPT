import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time

def get_stock_info(stock_code, update_count):
    # UserAgent 객체 생성
    ua = UserAgent()
    
    # Yahoo Finance URL 및 검색 쿼리
    url = "https://finance.yahoo.com"
    search_query = "/quote/"
    
    for i in range(update_count):
        try:
            # UserAgent를 이용한 랜덤한 HTTP 헤더 생성
            headers = {'User-Agent': ua.random}
            
            # Yahoo Finance의 검색 결과 페이지에서 해당 주식 페이지로 이동하여 HTML 가져오기
            response = requests.get(url + search_query + stock_code, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            # 주식 정보 가져오기
            price_element = soup.select_one("#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\).W\(100\%\) > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div.D\(ib\).Mend\(20px\) > fin-streamer.Fw\(b\).Fz\(36px\).Mb\(-4px\).D\(ib\)")
            price = price_element.text if price_element is not None else "N/A"
            
            change_element = soup.select_one("#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\).W\(100\%\) > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div.D\(ib\).Mend\(20px\) > fin-streamer:nth-child(2) > span")
            change = change_element.text if change_element is not None else "N/A"
            
            change_percent_element = soup.select_one("#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\).W\(100\%\) > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div.D\(ib\).Mend\(20px\) > fin-streamer:nth-child(3) > span")
            change_percent = change_percent_element.text if change_percent_element is not None else "N/A"
          

       # 결과 출력
            print(f"{stock_code}: {price} ({change}), Change Percent: {change_percent}")
        except:
            print(f"{stock_code}: Error: Request failed")

        # 1분 간격으로 실행
        time.sleep(60)

# 메인에서 사용 시
# get_stock_info("AAPL", 5)