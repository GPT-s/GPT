import requests
from bs4 import BeautifulSoup
import random
import time
from fake_useragent import UserAgent

def get_stock_info(stock_code, num_updates):
    user_agent = UserAgent()

    url = "https://finance.yahoo.com"
    search_query = "/quote/"
    
    for i in range(num_updates):
        try:
            headers = {"User-Agent": user_agent.random}
            
            response = requests.get(url + search_query + stock_code, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            price_element = soup.select_one("#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\).W\(100\%\) > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div.D\(ib\).Mend\(20px\) > fin-streamer:nth-child(3) > span")
            price = price_element.text if price_element is not None else "N/A"

            change_element = soup.select_one("#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\).W\(100\%\) > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div.Fz\(12px\).C\(\$tertiaryColor\).My\(0px\).D\(ib\).Va\(b\) > span.Fw\(500\) > fin-streamer:nth-child(2) > span")
            change = change_element.text if change_element is not None else "N/A"

            print(f"{stock_code}: {price} ({change})")

        except:
            print(f"Error: Failed to get stock info for {stock_code}")

        time.sleep(60)
