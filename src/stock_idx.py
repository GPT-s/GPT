import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def get_stock_info(stock_symbol):
    url = f"https://finance.yahoo.com/quote/{stock_symbol}"
    headers = {"User-Agent": UserAgent().random}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        price = soup.select_one('#quote-header-info > div > div > div > span[data-reactid="32"]').text
        change = soup.select_one('#quote-header-info > div > div > div > span[data-reactid="50"]').text
        print(f"Price: {price}")
        print(f"Change: {change}")
    except:
        print("Error: Request failed")

# main에서 실행 시
# import stock_idx

# yahoo_finance.get_stock_info("AAPL")  

# AAPL에 원하는 종목 이름 
