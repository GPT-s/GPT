import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time

def get_stock_info(stock_code, update_count):
    ua = UserAgent()
    
    url = "https://finance.yahoo.com"
    search_query = "/quote/"
    
    for i in range(update_count):
        try:
            headers = {'User-Agent': ua.random}
            
            response = requests.get(url + search_query + stock_code, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            price_element = soup.select_one("#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\).W\(100\%\) > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div.D\(ib\).Mend\(20px\) > fin-streamer.Fw\(b\).Fz\(36px\).Mb\(-4px\).D\(ib\)")
            price = price_element.text if price_element is not None else "N/A"
            
            change_element = soup.select_one("#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\).W\(100\%\) > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div.D\(ib\).Mend\(20px\) > fin-streamer:nth-child(2) > span")
            change = change_element.text if change_element is not None else "N/A"
            
            change_percent_element = soup.select_one("#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\).W\(100\%\) > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div.D\(ib\).Mend\(20px\) > fin-streamer:nth-child(3) > span")
            change_percent = change_percent_element.text if change_percent_element is not None else "N/A"
          

            print(f"{stock_code}: {price} ({change}), Change Percent: {change_percent}")
        except:
            print(f"{stock_code}: Error: Request failed")

        time.sleep(60)

# 메인에서 사용 시
# get_stock_info("AAPL", 5)  "AAPL"부분 주식코드 필요함