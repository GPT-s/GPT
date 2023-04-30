from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import requests
from bs4 import BeautifulSoup
import time
import logging
import asyncio
import time
import os


logging.basicConfig(filename="stockidx.log", level=logging.ERROR)

start_time = time.time()
class StockData:
    def __init__(self, location):
        self.location = location
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'}

    async def get_stock_info(self, location):
        max_retries = 5
        retries = 0
        while retries < max_retries:
            try:
                url = "https://finance.yahoo.com/quote/"
                response = requests.get(url + location, headers=self.headers)
                soup = BeautifulSoup(response.content, 'html.parser')

                price_element = soup.select_one("#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\).W\(100\%\) > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div.D\(ib\).Mend\(20px\) > fin-streamer.Fw\(b\).Fz\(36px\).Mb\(-4px\).D\(ib\)")
                price = price_element.text if price_element is not None else "N/A"

                change_element = soup.select_one("#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\).W\(100\%\) > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div.D\(ib\).Mend\(20px\) > fin-streamer:nth-child(2) > span")
                change = change_element.text if change_element is not None else "N/A"

                change_percent_element = soup.select_one("#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\).W\(100\%\) > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div.D\(ib\).Mend\(20px\) > fin-streamer:nth-child(3) > span")
                change_percent = change_percent_element.text if change_percent_element is not None else "N/A"


                stocktext = f"주식종목 :  [{self.location}] │ 현재가 :  {price} │ 변동 :  {change} │ 변동률 :  {change_percent}"
                return stocktext
            except Exception as e:
                print("Error:", e)
                retries += 1
                if retries == max_retries:
                    print("최대 재시도 횟수 초과")
                    gpt_error = "오류"
                    return gpt_error
        

    async def screenshot(self, location):
        max_retries = 5
        retries = 0
        while retries < max_retries:
            try:
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument('--start-maximized')
                chrome_options.add_argument(f'headers={self.headers}')
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
                driver.get(url = f'https://finance.yahoo.com/quote/{location}')
                time.sleep(5)
                x_btn = driver.find_element(By.CSS_SELECTOR, '#dropdown-menu > button > svg')
                x_btn.click()
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                folder_path = os.path.join(desktop_path, "stockimg")
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                    print("폴더가 생성되었습니다.")
                else:
                    print("이미 폴더가 존재합니다.")
                path = os.path.join(folder_path, f"{location}.png")
                driver.find_element(By.ID, 'interactive-2col-qsp-m').screenshot(path)
                driver.quit()
                return path
            except Exception as e:
                print("Error:", e)
                retries += 1
                if retries == max_retries:
                    print("최대 재시도 횟수 초과")
                    gpt_error = "오류"
                    return gpt_error
                
    
end_time = time.time()
total_time = end_time - start_time 
print(f'걸린 시간 : {total_time : .2f}')
#메인에서 사용 시 
locations = ['NFLX', 'AAPL', 'TSLA', 'FB']
stocks = [StockData(location) for location in locations]

# for location in locations:
#     stock = StockData(location)
#     screenshot_path = stock.screenshot(location)
#     logging.info('스크린샷 저장 완료')

# stock.screenshot("stock_screenshot.jpg")

# 메인에서 사용 시 
async def main():
    coroutines = []
    for stock in stocks:
        coroutines.append(stock.get_stock_info(stock.location))
        coroutines.append(stock.screenshot(stock.location))
        
        results = await asyncio.gather(*coroutines)

        for result in result :
            print(result)

asyncio.run(main())
