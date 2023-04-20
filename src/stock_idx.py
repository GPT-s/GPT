import requests
from bs4 import BeautifulSoup
import time
import logging

# def get_stock_info(stock_code, update_count):
#     url = "https://finance.yahoo.com"
#     search_query = "/quote/"
    
#     for i in range(update_count):
#         try:
#             headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'}
            
#             response = requests.get(url + search_query + stock_code, headers=headers)
#             soup = BeautifulSoup(response.content, 'html.parser')

#             price_element = soup.select_one("#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\).W\(100\%\) > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div.D\(ib\).Mend\(20px\) > fin-streamer.Fw\(b\).Fz\(36px\).Mb\(-4px\).D\(ib\)")
#             price = price_element.text if price_element is not None else "N/A"
            
#             change_element = soup.select_one("#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\).W\(100\%\) > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div.D\(ib\).Mend\(20px\) > fin-streamer:nth-child(2) > span")
#             change = change_element.text if change_element is not None else "N/A"
            
#             change_percent_element = soup.select_one("#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\).W\(100\%\) > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div.D\(ib\).Mend\(20px\) > fin-streamer:nth-child(3) > span")
#             change_percent = change_percent_element.text if change_percent_element is not None else "N/A"

#             print(f"{stock_code}: {price} ({change}), Change Percent: {change_percent}")
#         except:
#             print(f"{stock_code}: Error:  안돼용")

#         time.sleep(60)

# Usage: 
# get_stock_info("AAPL", 5)  # "AAPL" 부분 주식코드 필요

class StockData:
    def __init__(self, stock_code):
        self.stock_code = stock_code

    def get_stock_info(self, update_count):
        url = "https://finance.yahoo.com"
        search_query = "/quote/"

        for i in range(update_count):
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'}

                response = requests.get(url + search_query + self.stock_code, headers=headers)
                soup = BeautifulSoup(response.content, 'html.parser')

                price_element = soup.select_one("#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\).W\(100\%\) > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div.D\(ib\).Mend\(20px\) > fin-streamer.Fw\(b\).Fz\(36px\).Mb\(-4px\).D\(ib\)")
                price = price_element.text if price_element is not None else "N/A"

                change_element = soup.select_one("#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\).W\(100\%\) > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div.D\(ib\).Mend\(20px\) > fin-streamer:nth-child(2) > span")
                change = change_element.text if change_element is not None else "N/A"

                change_percent_element = soup.select_one("#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\).W\(100\%\) > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div.D\(ib\).Mend\(20px\) > fin-streamer:nth-child(3) > span")
                change_percent = change_percent_element.text if change_percent_element is not None else "N/A"

                print(f"{self.stock_code}: {price} ({change}), Change Percent: {change_percent}")
                logging.info('출력성공')
            except:
                print(f"{self.stock_code}: Error:  안돼용")
                logging.info('안됨')

            time.sleep(60)

stock = StockData("AAPL")
stock.get_stock_info(5)  # Fetch stock info for 5 updates




