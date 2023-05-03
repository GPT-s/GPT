from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import requests
from bs4 import BeautifulSoup
import time
import logging
import time
import os

import asyncio
import aiohttp

logging.basicConfig(filename="stockIdx.log", level=logging.ERROR)
start = time.time()

class StockData:
    def __init__(self, location):
        self.location = location
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'}
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument(f'headers={self.headers}')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    async def get_stock_info(self, location):
        max_retries = 5
        retries = 0
        while retries < max_retries:
            try:
                url = "https://finance.yahoo.com/quote/"
                async with aiohttp.ClientSession(headers=self.headers) as session:
                    async with session.get(url + location) as response:
                        content = await response.text()
                soup = BeautifulSoup(content, 'html.parser')

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
                    logging.error("지수크롤링 :최대 재시도 횟수 초과")
                    gpt_error = "오류"
                    return gpt_error
        

    async def screenshot(self, location):
        max_retries = 5
        retries = 0
        while retries < max_retries:
            try:
                self.driver.get(url = f'https://finance.yahoo.com/quote/{location}')
                await asyncio.sleep(1)
                x_btn = self.driver.find_element(By.CSS_SELECTOR, '#dropdown-menu > button > svg')
                x_btn.click()
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                folder_path = os.path.join(desktop_path, "stockimg")
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                    print("폴더가 생성되었습니다.")
                else:
                    print("이미 폴더가 존재합니다.")
                path = os.path.join(folder_path, f"{location}.png")
                self.driver.find_element(By.ID, 'interactive-2col-qsp-m').screenshot(path)
                self.driver.quit()
                return path
            except Exception as e:
                print("Error:", e)
                retries += 1
                if retries == max_retries:
                    logging.error("스크린샷 :최대 재시도 횟수 초과")
                    gpt_error = "오류"
                    return gpt_error
                

async def main():
    locations = ['AAPL', 'GOOGL', 'AMZN','TSLA']
    tasks = []
    for location in locations:
        stock = StockData(location)
        task1 = asyncio.ensure_future(stock.get_stock_info(location))
        task2 = asyncio.ensure_future(stock.screenshot(location))
        tasks.append(task1)
        tasks.append(task2)
    results = await asyncio.gather(*tasks, return_exceptions=True)
    print(results)

asyncio.run(main())



# async def main():
#     stock_data = StockData("AAPL")
#     tasks = [
#     asyncio.create_task(stock_data.get_stock_info("AAPL")),
#     asyncio.create_task(stock_data.screenshot("AAPL"))
#     ]
#     results = await asyncio.gather(*tasks)
#     stock_text = results[0]
#     screenshot_path = results[1]
#     print(stock_text)
#     print(screenshot_path)

# asyncio.run(main())

# end = time.time()
# print(f"총 실행 시간 : {end-start}")
            

                
        
                


    # locations = ['NFLX', 'AAPL', 'TSLA', 'FB']
    # stocks = [StockData(location) for location in locations]

    # end = time.time()
    # t_time = end - start
    # #     print(t_time)
    # # locations = ['NFLX', 'AAPL', 'TSLA', 'FB']
    # # stocks = [StockData(location) for location in locations]

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(asyncio.gather(get_stock_info(), get_stock_info(), screenshot()))
    # loop.close()
    # print(t_time)

# asyncio.run(main())
# asyncio.run(main())
# asyncio.run(main())





# async def gather_stock_info(stock):
#     return await stock.get_stock_info(stock.location)

# async def gather_screenshot(stock):
#     return await stock.screenshot(stock.location)

# async def main():
#     locations = ['NFLX', 'AAPL', 'TSLA', 'FB']
#     stocks = [StockData(location) for location in locations]

#     stock_info_tasks = [asyncio.create_task(gather_stock_info(stock)) for stock in stocks]
#     screenshot_tasks = [asyncio.create_task(gather_screenshot(stock)) for stock in stocks]

#     stock_info_results = await asyncio.gather(*stock_info_tasks)
#     screenshot_results = await asyncio.gather(*screenshot_tasks)




#     stock_info_results, screenshot_results = await asyncio.gather(*stock_info_tasks, *screenshot_tasks)
#     for i in range(len(stocks)):
#         print(stock_info_results[i])
#         print(screenshot_results[i])

#     print('완료')

# asyncio.run(main())
# asyncio.run(main())
# print("222222")
# asyncio.run(main())
# print("3333333")

