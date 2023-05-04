from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import requests
from bs4 import BeautifulSoup as bs
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import logging
import pymysql
import pymysql.err
import asyncio
import time




os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

class AsyncLiveCrawler:
    def __init__(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
    
    async def set_chrome_driver(self, headless=True):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("headless")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
        )
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        return driver

    async def investing_crawl_page(self, url):
        max_retries = 5
        retries = 0
        while retries < max_retries:
            try:
                driver = await self.set_chrome_driver(True)
                driver.get(url)
                article_page = driver.find_element(By.CLASS_NAME, "articlePage")
                text = article_page.text
                driver.close()
                return text
            except Exception as e:
                print("Error:", e)
                retries += 1
                if retries == max_retries:
                    print("최대 재시도 횟수 초과1")
                    gpt_error = "오류1"
                    return gpt_error

    async def investing_search(self, news):
        max_retries = 5
        retries = 0
        while retries < max_retries:
            try:
                investing_stock_latest = await self.set_chrome_driver(True)
                investing_stock_latest.get("https://www.investing.com/")
                search = investing_stock_latest.find_element(By.CSS_SELECTOR, ".js-main-search-bar")
                search.send_keys(news)  
                search.send_keys(Keys.ENTER)
                div_name = investing_stock_latest.find_element(
                    By.CSS_SELECTOR, ".js-inner-all-results-quotes-wrapper"
                )
                a_name = div_name.find_element(By.CSS_SELECTOR, "a")
                a_name.click()
                a_name2 = investing_stock_latest.find_element(
                    By.CSS_SELECTOR, 'a[data-test="link-news"]'
                )
                a_name2.click()

                element = investing_stock_latest.find_elements(By.CSS_SELECTOR, "section > div.mediumTitle1 > article.js-article-item.articleItem")
                data_id = element[0].get_attribute('data-id')
                investing_stock_latest_links = f'https://www.investing.com/news/economy/us-and-south-korea-agree-to-minimise-chipmakers-uncertainties-on-subsidy-requirements-ministry-{data_id}'
                print(investing_stock_latest_links)
                print(data_id)
                investing_stock_latest.quit()
                return investing_stock_latest_links
            except Exception as e:
                print("Error:", e)
                retries += 1
                if retries == max_retries:
                    print("최대 재시도 횟수 초과2")
                    gpt_error = "오류2"
                    return gpt_error
                
                
# 메인에서 사용
# async def main():
#     st_time = time.time()
#     crawler = AsyncLiveCrawler()
#     links = await crawler.investing_search("AAPL")
#     text = await crawler.investing_crawl_page(links)
#     print(text)
#     ed_time = time.time()
#     to_time = ed_time - st_time
#     print(f"걸린 시간 : {to_time:2f}초 ")

# asyncio.run(main())
